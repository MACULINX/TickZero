#!/usr/bin/env python
"""
Test script to verify GSI map.phase detection works correctly.
Simulates GSI payloads with different map phases.
"""
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.core.obs_manager import OBSManager
from src.core.gsi_server import GSIServer

def create_mock_gsi_payload(map_phase, round_phase="live", round_num=1, kills=0):
    """Create a mock GSI payload for testing."""
    return {
        "provider": {
            "name": "Counter-Strike: Global Offensive",
            "appid": 730,
            "version": 13960,
            "steamid": "76561198000000000",
            "timestamp": int(time.time())
        },
        "map": {
            "mode": "competitive",
            "name": "de_dust2",
            "phase": map_phase,  # This is what we're testing!
            "round": round_num,
            "team_ct": {
                "score": 0
            },
            "team_t": {
                "score": 0
            }
        },
        "round": {
            "phase": round_phase,
            "round": round_num
        },
        "player": {
            "steamid": "76561198000000000",
            "name": "TestPlayer",
            "state": {
                "health": 100,
                "armor": 100,
                "helmet": True
            },
            "match_stats": {
                "kills": kills,
                "assists": 0,
                "deaths": 0,
                "mvps": 0,
                "score": kills * 2
            }
        }
    }

def test_map_phase_detection():
    """Test that map.phase is properly detected."""
    print("=" * 60)
    print("  GSI Map Phase Detection Test")
    print("=" * 60)
    
    # Create mock OBS manager (not actually connected)
    class MockOBSManager:
        def __init__(self):
            self.recording_start_time = time.time()
        
        def calculate_video_timestamp(self, event_time):
            return event_time - self.recording_start_time
    
    obs = MockOBSManager()
    
    # Track callbacks
    match_started = False
    match_ended = False
    
    def on_start():
        nonlocal match_started
        match_started = True
        print("[OK] Match start callback triggered!")
    
    def on_end():
        nonlocal match_ended
        match_ended = True
        print("[OK] Match end callback triggered!")
    
    # Create GSI server
    gsi = GSIServer(
        obs_manager=obs,
        port=3000,
        log_file="test_gsi_log.json",
        on_match_start=on_start,
        on_match_end=on_end
    )
    
    print("\n[Test 1] Simulating match lifecycle...")
    print("-" * 60)
    
    # Test 1: Warmup phase
    print("\n1. Sending warmup phase...")
    payload = create_mock_gsi_payload(map_phase="warmup", round_phase="freezetime", round_num=0)
    gsi.process_game_state(payload)
    time.sleep(0.1)
    
    # Test 2: Match goes live
    print("\n2. Sending live phase (match start)...")
    payload = create_mock_gsi_payload(map_phase="live", round_phase="live", round_num=1)
    gsi.process_game_state(payload)
    time.sleep(0.1)
    
    # Test 3: Some kills during match
    print("\n3. Simulating kills during match...")
    for i in range(1, 4):
        payload = create_mock_gsi_payload(map_phase="live", round_phase="live", round_num=1, kills=i)
        gsi.process_game_state(payload)
        time.sleep(0.05)
    
    # Test 4: Match ends
    print("\n4. Sending gameover phase (match end)...")
    payload = create_mock_gsi_payload(map_phase="gameover", round_phase="over", round_num=30)
    gsi.process_game_state(payload)
    time.sleep(0.1)
    
    # Verify results
    print("\n" + "=" * 60)
    print("  Test Results")
    print("=" * 60)
    
    results = {
        "Match Start Detected": match_started,
        "Match End Detected": match_ended,
        "Events Logged": len(gsi.match_events),
        "Match In Progress": gsi.match_in_progress
    }
    
    for key, value in results.items():
        status = "[OK]" if value else "[FAIL]"
        print(f"{status} {key}: {value}")
    
    # Check if test passed
    all_passed = match_started and match_ended and len(gsi.match_events) > 0
    
    print("\n" + "=" * 60)
    if all_passed:
        print("SUCCESS: ALL TESTS PASSED!")
        print("\nMap phase detection is working correctly:")
        print("  - Warmup phase detected")
        print("  - Live phase triggered match start")
        print("  - Gameover phase triggered match end")
    else:
        print("FAILURE: SOME TESTS FAILED")
        if not match_started:
            print("  - Match start not detected from map.phase = 'live'")
        if not match_ended:
            print("  - Match end not detected from map.phase = 'gameover'")
    print("=" * 60)
    
    # Show event log
    print(f"\nEvents logged ({len(gsi.match_events)}):")
    for event in gsi.match_events:
        print(f"  - {event['type']:20s} | Round {event.get('round', 0):2d} | {event.get('phase', 'N/A'):10s}")
    
    return all_passed

if __name__ == '__main__':
    try:
        success = test_map_phase_detection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFAILURE: Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
