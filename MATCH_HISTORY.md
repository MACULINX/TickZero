# Match History System - User Guide

## Quick Start

### 1. Automatic Mode (Recommended)

The match history system automatically tracks all your matches:

```bash
# Start recording with auto-tracking
python main.py live
```

Each match is automatically:
- ✅ Saved to database (`matches.db`)
- ✅ Linked to video file
- ✅ Linked to match log
- ✅ Statistics extracted (kills, rounds, duration)

### 2. Browse Match History

Start the web interface:

```bash
python web_interface.py
```

Then open: **http://localhost:5000**

### 3. Generate Highlights

From the web interface:
1. Browse match list
2. Click on a match
3. Click "Generate Highlights"
4. Wait for processing to complete

## Web Interface Features

### Dashboard
- Overall statistics (total matches, kills, playtime)
- Recent matches list
- Quick access to pending matches

### Match List
- Full history of all recorded matches
- Sort and filter options
- K/D ratio, rounds played, duration

### Match Detail
- Complete event timeline
- Video and log file paths
- Per-match statistics
- One-click highlight generation
- Match deletion

## Configuration

Add to `main.py` config:

```python
config = {
    # ... existing config ...
    'db_path': 'matches.db',           # Database file path
    'web_interface_port': 5000,        # Web UI port
}
```

## Database Schema

### matches table
- Video file path
- Match log path
- Duration, kills, deaths, rounds
- Processing status
- Timestamps

### highlights table
- Links generated clips to matches
- Timestamp ranges
- Priority scores

## Workflow Example

```
1. Play CS2 → Match auto-recorded and saved
2. Repeat for multiple matches
3. Open web UI → Browse history
4. Select interesting match → Generate highlights
5. Clips saved to highlights/ folder
```

## Benefits

- ✅ **Never lose a match**: Automatic database tracking
- ✅ **Process anytime**: Generate highlights days/weeks later
- ✅ **Easy browsing**: Visual timeline of all matches
- ✅ **Statistics**: Track progress over time
- ✅ **Organized**: No manual file management needed
