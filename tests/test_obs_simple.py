#!/usr/bin/env python
"""
Quick verification script to check if OBS test was successful.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.obs_manager import OBSManager
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Test just the connection
obs = OBSManager(
    host=config['obs_host'],
    port=config['obs_port'],
    password=config.get('obs_password', '')
)

print("Testing OBS connection...")
if obs.connect():
    print("✓ OBS WebSocket connection: SUCCESS")
    
    # Get current status
    status = obs.get_recording_status()
    print(f"✓ Recording status query: SUCCESS")
    print(f"  Currently recording: {status['is_recording']}")
    
    obs.disconnect()
    print("\n✅ Basic OBS integration is working!")
else:
    print("❌ Cannot connect to OBS")
    print("Make sure OBS is running with WebSocket enabled")
