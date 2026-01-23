"""
AI Director Module.

Uses Google Gemini with a ReAct (Reasoning + Acting) pattern to analyze match logs 
and identify highlight-worthy moments in CS2 gameplay.
"""
import json
import logging
import os
import re
from typing import List, Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    # Handle missing dependency gracefully for type checking
    genai = Any
    types = Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIDirector:
    """
    Analyzes game events using Gemini with ReAct pattern.
    
    Implementation follows a strict Chain-of-Thought process:
    Thought -> Reasoning -> Action -> Observation -> Final Output
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize AI Director.
        
        Args:
            api_key: Google API Key. If None, reads from GOOGLE_API_KEY env var.
            model: Gemini model name.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("No Google API Key provided. Set GOOGLE_API_KEY environment variable.")
            
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                
        self.model_name = model
        
    def analyze_match_log(self, log_path: str) -> List[Dict[str, Any]]:
        """
        Analyze a match log file to identify highlights.
        
        Args:
            log_path: Path to the match_log.json file.
            
        Returns:
            List of highlight dictionaries containing start_time, end_time, label, score.
        """
        if not self.client:
            logger.error("AI Director cannot analyze: No API client initialized.")
            return []
            
        try:
            with open(log_path, 'r') as f:
                match_data = json.load(f)
                
            # Optimize: If log is too large, maybe split by rounds?
            # For now, sending the whole log (or relevant events)
            events = match_data.get('events', [])
            if not events:
                logger.warning("No events found in log.")
                return []
                
            # Construct the ReAct prompt
            prompt = self._construct_prompt(events)
            
            # Call Gemini
            logger.info(f"Sending analysis request to {self.model_name}...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, # Low temperature for more deterministic logic
                    max_output_tokens=4096
                )
            )
            
            # Parse response
            highlights = self._parse_response(response.text)
            logger.info(f"✓ AI Director identified {len(highlights)} highlights.")
            
            return highlights
            
        except Exception as e:
            logger.error(f"Error during match analysis: {e}")
            return []

    def _construct_prompt(self, events: List[Dict[str, Any]]) -> str:
        """
        Constructs the strict ReAct system prompt and inputs.
        """
        # Convert specific event types to a more readable format for the LLM
        # to save tokens and improve clarity
        formatted_events = []
        for e in events:
            # We focus on kills and round phases mostly
            if e.get('type') == 'kill':
                formatted_events.append(
                    f"[{e.get('video_time', 0):.2f}s] KILL: {e.get('attacker_name')} -> {e.get('victim_name')} "
                    f"({e.get('weapon')}{', HS' if e.get('is_headshot') else ''})"
                )
            elif e.get('type') == 'round_start':
                formatted_events.append(f"[{e.get('video_time', 0):.2f}s] ROUND START {e.get('round_number')}")
            elif e.get('type') == 'round_end':
                formatted_events.append(f"[{e.get('video_time', 0):.2f}s] ROUND END {e.get('round_number')} (Winner: {e.get('winner')})")
                
        events_str = "\n".join(formatted_events)

        system_prompt = """Sei un analista esperto di Counter-Strike 2. Il tuo compito è identificare highlight nel log JSON fornito.
Devi seguire un processo di pensiero rigoroso (Chain-of-Thought) prima di emettere il risultato JSON finale.

FORMATO DI RISPOSTA OBBLIGATORIO:
Thought: [Analisi del contesto. Es: 'Il giocatore ha fatto 3 kill in 10 secondi?']
Reasoning: [Valutazione della qualità. Es: 'Erano headshot? La salute era bassa (Clutch)?']
Action: [Decisione. Es: 'Seleziona clip da T-5s a T+2s']
Observation: [Verifica sovrapposizioni. Es: 'Questo clip si sovrappone al precedente? Uniscili.']
Final Output: [Array JSON con {start_time, end_time, label, score}]

CRITERI DI SELEZIONE:
1. Multi-kill (3+ kill in <15s) -> Priorità Alta.
2. Clutch (1vsX vinto) -> Priorità Massima.
3. Knife Kills / Zeus -> Priorità Media.

Ecco il log degli eventi della partita:
"""
        return f"{system_prompt}\n{events_str}\n\nAnalizza e fornisci il Final Output."

    def _parse_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parses the ReAct response to extract only the Final Output JSON.
        """
        try:
            # Flexible pattern matching to find the JSON array in the Final Output section
            # Look for "Final Output:" followed by array brackets
            # Pattern accounts for potential markdown code blocks ```json ... ```
            
            # First, try to locate "Final Output" label
            parts = response_text.split("Final Output:")
            if len(parts) < 2:
                logger.warning("Could not find 'Final Output:' section in response.")
                # Fallback: try to find the last JSON code block
                json_candidates = re.findall(r'```(?:json)?\s*(\[.*?\])\s*```', response_text, re.DOTALL)
                if json_candidates:
                    return json.loads(json_candidates[-1])
                return []
                
            final_section = parts[-1].strip()
            
            # Check for markdown code block in the final section
            code_block_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', final_section, re.DOTALL)
            if code_block_match:
                json_str = code_block_match.group(1)
            else:
                # Try to find the first '[' and last ']'
                start = final_section.find('[')
                end = final_section.rfind(']')
                if start != -1 and end != -1:
                    json_str = final_section[start:end+1]
                else:
                    logger.warning("No JSON array found in Final Output section.")
                    return []
            
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from AI response: {e}")
            logger.debug(f"Response text start: {response_text[:200]}...")
            return []
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return []
