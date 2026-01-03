"""
Example: Quick test of OBS connection and recording start.
This script demonstrates how to use OBSManager independently.
"""
from obs_manager import OBSManager
import time

def test_obs_connection():
    """Test OBS WebSocket connection and recording."""
    
    print("=" * 60)
    print("OBS CONNECTION TEST")
    print("=" * 60)
    
    # Initialize OBS Manager
    obs = OBSManager(host="localhost", port=4455, password="")
    
    # Connect to OBS
    print("\n[1] Connecting to OBS...")
    if not obs.connect():
        print("❌ Failed to connect. Make sure:")
        print("   - OBS is running")
        print("   - WebSocket Server is enabled (Tools → WebSocket Server Settings)")
        print("   - Port and password match your OBS settings")
        return
    
    # Get current recording status
    print("\n[2] Checking recording status...")
    status = obs.get_recording_status()
    print(f"   Currently recording: {status['is_recording']}")
    
    # Start recording if not already recording
    if not status['is_recording']:
        print("\n[3] Starting recording...")
        start_time = obs.start_recording()
        
        if start_time:
            print(f"   ✓ Recording started!")
            print(f"   ✓ Start timestamp (T=0): {start_time}")
            
            # Simulate some events
            print("\n[4] Simulating events...")
            for i in range(3):
                time.sleep(2)
                current_time = time.time()
                video_time = obs.calculate_video_timestamp(current_time)
                print(f"   Event {i+1} at video timestamp: {video_time:.2f}s")
            
            # Stop recording
            print("\n[5] Stopping recording...")
            obs.stop_recording()
            print("   ✓ Recording stopped")
    else:
        print("   ℹ Already recording, skipping start test")
    
    # Disconnect
    print("\n[6] Disconnecting...")
    obs.disconnect()
    
    print("\n" + "=" * 60)
    print("✓ TEST COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    test_obs_connection()
