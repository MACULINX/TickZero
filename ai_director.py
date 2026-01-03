"""
AIDirector: Uses LLM to analyze game events and identify highlight-worthy segments.
Processes match logs and returns timestamp ranges for video cuts.
"""
import json
import logging
import google.generativeai as genai
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIDirector:
    """Analyzes game events using LLM to identify highlight moments."""
    
    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        """
        Initialize AI Director with Google Gemini.
        
        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env variable)
            model: Gemini model to use (default: gemini-1.5-flash - FREE with daily quota)
                   Options: gemini-1.5-flash (fast, free), gemini-1.5-pro (more capable)
        """
        # Configure Gemini
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from environment
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
            else:
                logger.warning("No API key provided. Set GOOGLE_API_KEY environment variable.")
        
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        
    def analyze_match_log(self, log_file_path):
        """
        Analyze entire match log and identify all highlight segments.
        
        Args:
            log_file_path: Path to match_log.json
            
        Returns:
            list: Highlight segments with start/end times and labels
        """
        try:
            with open(log_file_path, 'r') as f:
                match_data = json.load(f)
            
            events = match_data.get('events', [])
            
            if not events:
                logger.warning("No events found in match log")
                return []
            
            # Group events by round
            rounds = self._group_events_by_round(events)
            
            all_highlights = []
            
            # Analyze each round
            for round_num, round_events in rounds.items():
                logger.info(f"Analyzing Round {round_num}...")
                highlights = self._analyze_round(round_num, round_events)
                all_highlights.extend(highlights)
            
            logger.info(f"✓ Identified {len(all_highlights)} highlight segments")
            return all_highlights
            
        except Exception as e:
            logger.error(f"Error analyzing match log: {e}")
            return []
    
    def _group_events_by_round(self, events):
        """Group events by round number."""
        rounds = {}
        for event in events:
            round_num = event.get('round', 0)
            if round_num not in rounds:
                rounds[round_num] = []
            rounds[round_num].append(event)
        return rounds
    
    def _analyze_round(self, round_num, events):
        """
        Use LLM to analyze a single round and identify highlights.
        
        Args:
            round_num: Round number
            events: List of events in this round
            
        Returns:
            list: Highlight segments for this round
        """
        # Prepare prompt for LLM
        prompt = self._create_analysis_prompt(round_num, events)
        
        # System instructions for Gemini
        system_instruction = """You are a CS2 highlight analyzer. Your job is to identify exciting moments worth clipping for TikTok/Reels.

HIGHLIGHT CRITERIA (priority order):
1. Multi-kills (2K, 3K, 4K, ACE) - The more kills in quick succession, the better
2. Clutch situations (1vX) - Especially if won
3. Headshot kills - Particularly one-taps
4. High-skill plays - Difficult shots, quick reactions
5. Low health clutches - Surviving with <20 HP

TIMING RULES:
- Start clip 2-3 seconds BEFORE first kill (for context)
- End clip 2-3 seconds AFTER last kill (for reaction)
- Keep clips 8-15 seconds (TikTok optimal length)
- If kills are >10s apart, create separate clips

OUTPUT FORMAT (JSON only):
{
  "highlights": [
    {
      "start": 120.5,
      "end": 133.2,
      "label": "3k_headshot",
      "priority": 9
    }
  ]
}

Priority scale: 1-10 (10 = must-clip ACE, 1 = skip)"""
        
        try:
            # Create full prompt with system instruction
            full_prompt = f"{system_instruction}\n\n{prompt}"
            
            # Generate response with Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    response_mime_type="application/json"
                )
            )
            
            # Parse LLM response
            response_text = response.text
            result = json.loads(response_text)
            
            # Handle different response formats
            highlights = result.get('highlights', result.get('clips', []))
            
            if not highlights:
                logger.info(f"  Round {round_num}: No highlights identified")
                return []
            
            logger.info(f"  Round {round_num}: Found {len(highlights)} highlight(s)")
            for h in highlights:
                logger.info(f"    • {h.get('label')} ({h.get('start'):.1f}s - {h.get('end'):.1f}s) [Priority: {h.get('priority', 5)}]")
            
            return highlights
            
        except Exception as e:
            logger.error(f"Error calling LLM for round {round_num}: {e}")
            return []
    
    def _create_analysis_prompt(self, round_num, events):
        """
        Create detailed prompt for LLM analysis.
        
        Args:
            round_num: Round number
            events: Events in this round
            
        Returns:
            str: Formatted prompt
        """
        # Format events for clarity
        formatted_events = []
        for event in events:
            if event['type'] == 'kill':
                formatted_events.append(
                    f"[{event['video_time']:.1f}s] KILL - Weapon: {event['weapon']}, "
                    f"Headshot: {event['headshot']}, HP: {event['health']}, "
                    f"Total Kills: {event['total_kills']}"
                )
            elif event['type'] == 'round_phase_change':
                formatted_events.append(
                    f"[{event['video_time']:.1f}s] ROUND {event['phase'].upper()}"
                )
        
        prompt = f"""**ROUND {round_num} ANALYSIS**

Events (chronological):
{chr(10).join(formatted_events)}

Analyze these events and identify highlight-worthy moments. Consider:
- Are there multiple kills close together (multi-kill)?
- Any impressive headshots?
- Low health survival?
- Context: What makes this clip exciting?

Return JSON with highlight segments."""
        
        return prompt
    
    def filter_highlights_by_priority(self, highlights, min_priority=6):
        """
        Filter highlights by minimum priority score.
        
        Args:
            highlights: List of highlight segments
            min_priority: Minimum priority (1-10)
            
        Returns:
            list: Filtered highlights
        """
        filtered = [h for h in highlights if h.get('priority', 5) >= min_priority]
        logger.info(f"Filtered to {len(filtered)}/{len(highlights)} highlights (min priority: {min_priority})")
        return filtered
