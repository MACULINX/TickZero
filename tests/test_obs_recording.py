#!/usr/bin/env python
"""
Test script for OBS recording functionality.
Tests WebSocket connection, recording start/stop, and file path retrieval.
"""
import sys
import time
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.obs_manager import OBSManager

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_obs_recording():
    """Test OBS recording with a short clip."""
    
    print_header("OBS Recording Test")
    
    # Load config
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
    else:
        print("⚠ config.json not found, using defaults")
        config = {
            'obs_host': 'localhost',
            'obs_port': 4455,
            'obs_password': ''
        }
    
    # Initialize OBS Manager
    print(f"\n[1/5] Initializing OBS Manager...")
    print(f"  Host: {config['obs_host']}")
    print(f"  Port: {config['obs_port']}")
    
    obs = OBSManager(
        host=config['obs_host'],
        port=config['obs_port'],
        password=config.get('obs_password', '')
    )
    
    # Test connection
    print(f"\n[2/5] Testing OBS WebSocket connection...")
    if not obs.connect():
        print("❌ FAILED: Could not connect to OBS")
        print("\nTroubleshooting:")
        print("  1. Make sure OBS Studio is running")
        print("  2. Enable WebSocket Server in OBS: Tools → obs-websocket Settings")
        print(f"  3. Check that the port matches: {config['obs_port']}")
        print("  4. If you set a password in OBS, update config.json")
        return False
    
    print("✓ Connected successfully!")
    
    # Check current recording status
    status = obs.get_recording_status()
    if status['is_recording']:
        print("\n⚠ Recording is already in progress in OBS")
        print("  Stopping it first...")
        obs.stop_recording()
        time.sleep(1)
    
    # Start test recording
    print(f"\n[3/5] Starting test recording...")
    print("  Recording will run for 5 seconds...")
    
    start_time = obs.start_recording()
    if not start_time:
        print("❌ FAILED: Could not start recording")
        obs.disconnect()
        return False
    
    print(f"✓ Recording started at T={start_time}")
    
    # Record for 5 seconds
    for i in range(5, 0, -1):
        print(f"  Recording... {i}s remaining", end='\r')
        time.sleep(1)
    
    print("\n")
    
    # Stop recording
    print(f"[4/5] Stopping recording...")
    if not obs.stop_recording():
        print("❌ FAILED: Could not stop recording")
        obs.disconnect()
        return False
    
    print("✓ Recording stopped")
    
    # Get recording path
    print(f"\n[5/5] Checking recording file path...")
    recording_path = obs.get_last_recording_path()
    
    if recording_path:
        print(f"✓ Recording path retrieved: {recording_path}")
        
        # Check if file exists
        if Path(recording_path).exists():
            file_size = Path(recording_path).stat().st_size
            print(f"✓ File exists! Size: {file_size / 1024:.1f} KB")
        else:
            print(f"⚠ Path returned but file not found yet (may still be writing)")
            print(f"  Wait a moment and check: {recording_path}")
    else:
        print("⚠ Recording path not available")
        print("\nThis is a known limitation with some OBS versions.")
        print("The recording was successful, but you'll need to:")
        print("  1. Check OBS output folder manually")
        print("  2. Manually specify video path when processing highlights")
    
    # Disconnect
    obs.disconnect()
    
    # Final summary
    print_header("Test Summary")
    print(f"✓ OBS Connection: SUCCESS")
    print(f"✓ Start Recording: SUCCESS")
    print(f"✓ Stop Recording: SUCCESS")
    print(f"{'✓' if recording_path else '⚠'} Path Retrieval: {'SUCCESS' if recording_path else 'UNAVAILABLE (see above)'}")
    
    if recording_path and Path(recording_path).exists():
        print(f"\n🎉 All tests passed!")
        print(f"\nTest recording saved to:")
        print(f"  {recording_path}")
        print(f"\nYou can delete this test file if you don't need it.")
    else:
        print(f"\n⚠ Partial success - recording works but path retrieval needs manual verification")
    
    print("=" * 60 + "\n")
    
    return True

if __name__ == '__main__':
    try:
        test_obs_recording()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
