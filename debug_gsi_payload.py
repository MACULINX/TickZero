"""
Debug script to capture and analyze raw GSI payloads from CS2.
This helps diagnose whether kills are being tracked from multiple players.
"""
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DebugGSIHandler(BaseHTTPRequestHandler):
    """HTTP handler that logs all incoming GSI payloads."""
    
    payloads = []  # Store all received payloads
    
    def do_POST(self):
        """Handle incoming POST requests from CS2 GSI."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the payload
            game_state = json.loads(post_data.decode('utf-8'))
            timestamp = time.time()
            
            # Extract key information
            player_data = game_state.get('player', {})
            provider_data = game_state.get('provider', {})
            
            # Log payload summary
            logger.info("=" * 80)
            logger.info(f"📦 GSI PAYLOAD RECEIVED at {datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')}")
            
            # Check if this is player data or spectator data
            if 'steamid' in provider_data:
                logger.info(f"   Provider SteamID: {provider_data['steamid']}")
            
            if 'steamid' in player_data:
                logger.info(f"   Player SteamID: {player_data['steamid']}")
                logger.info(f"   Player Name: {player_data.get('name', 'Unknown')}")
            
            # Check for match stats
            if 'match_stats' in player_data:
                stats = player_data['match_stats']
                logger.info(f"   Kills: {stats.get('kills', 0)}")
                logger.info(f"   Deaths: {stats.get('deaths', 0)}")
                logger.info(f"   Assists: {stats.get('assists', 0)}")
            
            # Check for round info
            round_data = game_state.get('round', {})
            if 'phase' in round_data:
                logger.info(f"   Round Phase: {round_data['phase']}")
                logger.info(f"   Round Number: {round_data.get('round', 0)}")
            
            # Check if allplayers data is present (it shouldn't be!)
            if 'allplayers' in game_state:
                logger.warning("   ⚠️ ALLPLAYERS DATA DETECTED! This should not happen!")
                logger.warning(f"      Number of players: {len(game_state['allplayers'])}")
            
            logger.info("=" * 80)
            
            # Store payload for later analysis
            DebugGSIHandler.payloads.append({
                'timestamp': timestamp,
                'payload': game_state
            })
            
            # Send 200 OK
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            logger.error(f"Error processing GSI data: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default HTTP server logging."""
        pass


def main():
    """Run the debug GSI server."""
    port = 3000
    
    print("=" * 80)
    print("🔍 DEBUG GSI PAYLOAD ANALYZER")
    print("=" * 80)
    print(f"\nListening on port {port}")
    print("\nThis tool will capture and display all GSI payloads from CS2.")
    print("Pay attention to:")
    print("  1. Player SteamID - should be consistent (your SteamID)")
    print("  2. Kill increments - should only increase when YOU get a kill")
    print("  3. Allplayers data - should NOT be present")
    print("\nLaunch CS2 and play a match. Press Ctrl+C when done.")
    print("=" * 80)
    print()
    
    server = HTTPServer(('', port), DebugGSIHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nStopping server...")
        server.shutdown()
        
        # Save all payloads to file
        output_file = f"gsi_debug_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            json.dump(DebugGSIHandler.payloads, f, indent=2)
        
        print("\n" + "=" * 80)
        print("✓ DEBUG SESSION COMPLETE")
        print("=" * 80)
        print(f"Total payloads captured: {len(DebugGSIHandler.payloads)}")
        print(f"Saved to: {output_file}")
        print("=" * 80)


if __name__ == '__main__':
    main()
