"""
Example: Standalone GSI server test.
This allows you to verify CS2 GSI integration without OBS.
"""
from gsi_server import GSIServer
from obs_manager import OBSManager
import time

def test_gsi_server():
    """Test GSI server by running it standalone."""
    
    print("=" * 60)
    print("GSI SERVER TEST")
    print("=" * 60)
    print("\nThis will start the GSI server on port 3000.")
    print("Make sure you have copied gamestate_integration_highlights.cfg")
    print("to your CS2 cfg directory before testing.")
    print()
    print("CS2 cfg location:")
    print("C:\\Program Files (x86)\\Steam\\steamapps\\common\\")
    print("Counter-Strike Global Offensive\\game\\csgo\\cfg\\")
    print("=" * 60)
    
    # Create a mock OBS manager for timestamp calculation
    mock_obs = OBSManager()
    mock_obs.recording_start_time = time.time()
    
    print(f"\n✓ Mock recording start time: {mock_obs.recording_start_time}")
    
    # Create and start GSI server
    gsi = GSIServer(obs_manager=mock_obs, port=3000, log_file="test_match_log.json")
    gsi.start()
    
    print("\n" + "=" * 60)
    print("✓ GSI SERVER RUNNING")
    print("=" * 60)
    print("\nNow launch CS2 and play a match.")
    print("You should see events being logged in real-time.")
    print("\nPress Ctrl+C to stop the server.")
    print("=" * 60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping GSI server...")
        gsi.stop()
        
        print("\n" + "=" * 60)
        print("✓ TEST COMPLETE")
        print("=" * 60)
        print(f"\nCheck test_match_log.json for logged events")
        print(f"Total events captured: {len(gsi.match_events)}")
        print("=" * 60)


if __name__ == '__main__':
    test_gsi_server()
