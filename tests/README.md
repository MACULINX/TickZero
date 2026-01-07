# Test Scripts

This directory contains verification and testing scripts for the CS2 Highlights Generator.

## Test Scripts

### OBS WebSocket Tests
- **test_obs_simple.py** - Quick OBS WebSocket connection verification
- **test_obs_recording.py** - Full OBS recording test (5-second clip)

### GSI Tests
- **test_gsi_map_phase.py** - Verify map.phase detection for match end

### API Tests
- **test_api_key.py** - Verify Google API key environment variable

## Running Tests

```bash
# Quick OBS connection test
python tests/test_obs_simple.py

# Full OBS recording test
python tests/test_obs_recording.py

# GSI map phase detection test
python tests/test_gsi_map_phase.py

# API key verification
python tests/test_api_key.py
```

## Note

These tests are for development and verification. They are not required for normal operation of the application.
