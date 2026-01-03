"""
GSIServer: HTTP server that receives CS2 Game State Integration payloads.
Detects game events (kills, round changes) and logs them with video timestamps.
"""
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GSIServer:
    """Receives and processes CS2 Game State Integration data."""
    
    def __init__(self, obs_manager, port=3000, log_file="match_log.json", on_match_end=None):
        """
        Initialize GSI server.
        
        Args:
            obs_manager: OBSManager instance for timestamp synchronization
            port: Port to listen on (default: 3000)
            log_file: Path to save match log JSON
            on_match_end: Callback function called when match ends
        """
        self.port = port
        self.log_file = log_file
        self.obs_manager = obs_manager
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.on_match_end = on_match_end
        
        # Match state tracking
        self.previous_state = {}
        self.match_events = []
        self.current_round = 0
        self.last_round_phase = None
        self.match_ended = False
        self.rounds_since_event = 0  # Track inactivity
        
    def start(self):
        """Start the GSI HTTP server in a separate thread."""
        handler = self._create_handler()
        self.server = HTTPServer(('', self.port), handler)
        self.is_running = True
        
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        logger.info(f"✓ GSI Server listening on port {self.port}")
        logger.info(f"  Events will be logged to: {self.log_file}")
    
    def stop(self):
        """Stop the GSI server and save logs."""
        if self.server:
            self.server.shutdown()
            self.is_running = False
            logger.info("GSI Server stopped")
        
        self.save_logs()
    
    def _create_handler(self):
        """Create request handler with reference to this GSIServer instance."""
        gsi_server = self
        
        class GSIRequestHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                """Handle incoming POST requests from CS2."""
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                try:
                    # Parse CS2 JSON payload
                    game_state = json.loads(post_data.decode('utf-8'))
                    
                    # Process the game state
                    gsi_server.process_game_state(game_state)
                    
                    # Send 200 OK response
                    self.send_response(200)
                    self.end_headers()
                    
                except Exception as e:
                    logger.error(f"Error processing GSI data: {e}")
                    self.send_response(500)
                    self.end_headers()
            
            def log_message(self, format, *args):
                """Suppress default HTTP server logging."""
                pass
        
        return GSIRequestHandler
    
    def process_game_state(self, state):
        """
        Process incoming game state and detect events.
        
        Args:
            state: Parsed JSON game state from CS2
        """
        event_time = time.time()  # Capture system timestamp immediately
        
        try:
            # Extract key data from game state
            player_data = state.get('player', {})
            round_data = state.get('round', {})
            map_data = state.get('map', {})
            
            # Detect round phase changes
            if 'phase' in round_data:
                current_phase = round_data['phase']
                previous_phase = self.previous_state.get('round', {}).get('phase')
                
                if current_phase != previous_phase:
                    self._log_round_phase_change(event_time, current_phase, round_data)
            
            # Detect kills (by checking match_stats changes)
            if 'match_stats' in player_data:
                current_kills = player_data['match_stats'].get('kills', 0)
                previous_kills = self.previous_state.get('player', {}).get('match_stats', {}).get('kills', 0)
                
                if current_kills > previous_kills:
                    self._log_kill_event(event_time, player_data, round_data)
            
            # Update previous state for next comparison
            self.previous_state = state
            
        except Exception as e:
            logger.error(f"Error processing game state: {e}")
    
    def _log_round_phase_change(self, event_time, phase, round_data):
        """Log round phase changes and detect match end."""
        video_timestamp = self.obs_manager.calculate_video_timestamp(event_time)
        current_round = round_data.get('round', 0)
        
        event = {
            "type": "round_phase_change",
            "system_time": event_time,
            "video_time": video_timestamp,
            "datetime": datetime.fromtimestamp(event_time).strftime('%H:%M:%S.%f'),
            "phase": phase,
            "round": current_round
        }
        
        self.match_events.append(event)
        logger.info(f"📍 Round Phase: {phase} | Round: {current_round} | Video Time: {video_timestamp:.2f}s")
        
        # Detect match end: "gameover" phase or significant reset in rounds
        if phase == "gameover":
            logger.info("🏁 Match ended (gameover detected)")
            self._trigger_match_end()
        elif self.last_round_phase and current_round < self.current_round - 5:
            # Round number reset significantly (new match started)
            logger.info(f"🏁 New match detected (round reset from {self.current_round} to {current_round})")
            self._trigger_match_end()
        
        self.current_round = current_round
        self.last_round_phase = phase
    
    def _log_kill_event(self, event_time, player_data, round_data):
        """
        Log kill events with detailed context.
        
        Context includes:
        - Weapon used
        - Headshot (True/False)
        - Health remaining
        - Current round number
        """
        video_timestamp = self.obs_manager.calculate_video_timestamp(event_time)
        
        # Extract weapon and state information
        weapons = player_data.get('weapons', {})
        active_weapon = None
        for weapon_key, weapon_data in weapons.items():
            if weapon_data.get('state') == 'active':
                active_weapon = weapon_data.get('name', 'unknown')
                break
        
        state_data = player_data.get('state', {})
        match_stats = player_data.get('match_stats', {})
        
        event = {
            "type": "kill",
            "system_time": event_time,
            "video_time": video_timestamp,
            "datetime": datetime.fromtimestamp(event_time).strftime('%H:%M:%S.%f'),
            "round": round_data.get('round', 0),
            "weapon": active_weapon or "unknown",
            "headshot": match_stats.get('headshot_kills', 0) > self.previous_state.get('player', {}).get('match_stats', {}).get('headshot_kills', 0),
            "health": state_data.get('health', 0),
            "total_kills": match_stats.get('kills', 0)
        }
        
        self.match_events.append(event)
        logger.info(f"💀 Kill | Weapon: {event['weapon']} | HS: {event['headshot']} | HP: {event['health']} | Video Time: {video_timestamp:.2f}s")
    
    def _trigger_match_end(self):
        """Trigger match end callback."""
        if not self.match_ended and self.on_match_end:
            self.match_ended = True
            self.save_logs()
            # Call the callback (will trigger processing in background)
            self.on_match_end()
            # Reset for next match
            self.match_events = []
            self.match_ended = False
    
    def save_logs(self):
        """Save all logged events to JSON file."""
        try:
            log_data = {
                "recording_start_time": self.obs_manager.recording_start_time,
                "recording_start_datetime": datetime.fromtimestamp(self.obs_manager.recording_start_time).isoformat() if self.obs_manager.recording_start_time else None,
                "total_events": len(self.match_events),
                "events": self.match_events
            }
            
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            logger.info(f"✓ Saved {len(self.match_events)} events to {self.log_file}")
            
        except Exception as e:
            logger.error(f"✗ Failed to save logs: {e}")
    
    def get_events_by_round(self, round_number):
        """
        Get all events for a specific round.
        
        Args:
            round_number: Round number to filter
            
        Returns:
            list: Events from specified round
        """
        return [event for event in self.match_events if event.get('round') == round_number]
