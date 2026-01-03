# CS2 Capture-to-Content Pipeline

Automated highlight creation system for Counter-Strike 2 that converts gameplay into vertical (9:16) TikTok/Reels-ready clips using **FREE Google Gemini AI**.

## 🎯 Features

- **Live Event Logging**: Captures kills, headshots, and round events in real-time via CS2 GSI
- **OBS Synchronization**: Precise timestamp alignment between game events and video recording
- **AI-Powered Analysis**: Uses Google Gemini (FREE) to identify highlight-worthy moments
- **Automatic Video Editing**: FFmpeg-based conversion to vertical format with blurred background
- **Hardware Acceleration**: Supports NVIDIA NVENC with CPU fallback

## 📋 Requirements

### Software
- Python 3.10+
- OBS Studio (with WebSocket plugin enabled)
- FFmpeg (with hardware encoding support optional)
- Counter-Strike 2
- Google API key (Gemini - **FREE** with daily quota!)

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Setup

### 1. OBS WebSocket Configuration

1. Open OBS Studio
2. Go to **Tools → WebSocket Server Settings**
3. Enable WebSocket server
4. Note the port (default: 4455) and password (if set)
5. Update `config` in `main.py` if needed

### 2. CS2 Game State Integration

1. Copy `gamestate_integration_highlights.cfg` to:
   ```
   C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
   ```
   
2. Verify the `uri` points to `http://localhost:3000`

### 3. Google Gemini API Key (FREE!)

1. Get your free API key from: https://makersuite.google.com/app/apikey
2. Set it as environment variable:

```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY = "your-api-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

Or pass it directly when running post-processing.

**Note:** Gemini-1.5-Flash is FREE with generous daily quota (no credit card required)!

📖 **[Guida in Italiano per ottenere la chiave API Gemini →](SETUP_GEMINI.md)**


## 📖 Usage

The pipeline operates in **two distinct phases**:

### Phase 1: Live Logging (During Match)

Run this **BEFORE** starting your CS2 match:

```bash
python main.py live
```

This will:
1. Connect to OBS WebSocket
2. Start recording
3. Start GSI server on port 3000
4. Log all game events with precise video timestamps

**Play your match normally.** When finished, press `Ctrl+C` to stop logging.

Events are saved to `match_log.json`.

### Phase 2: Post-Processing (After Match)

Run this **AFTER** the match to create highlights:

```bash
python main.py process <path_to_recording.mp4> [api_key] [min_priority]
```

**Example:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" your-google-api-key 6
```

**Parameters:**
- `<path_to_recording.mp4>`: Path to OBS recording
- `[api_key]`: Google API key (optional if set as GOOGLE_API_KEY env variable)
- `[min_priority]`: Minimum clip priority 1-10 (default: 6)

This will:
1. Analyze `match_log.json` with AI
2. Identify highlight moments (multi-kills, clutches, etc.)
3. Create vertical video clips in `highlights/` directory

## 🎬 Output Format

**Vertical Video Specs:**
- Resolution: 1080x1920 (9:16)
- Format: MP4 (H.264)
- Audio: AAC stereo
- Visual: Blurred background + centered gameplay

**File Naming:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
```

## 🔧 Configuration

Edit `config` dict in `main.py`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,           # OBS WebSocket port
    'obs_password': '',         # OBS WebSocket password
    'gsi_port': 3000,           # GSI server port
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True             # Use NVENC if available
}
```

## 📊 How It Works

### Timestamp Synchronization

**Critical Concept**: The system maintains two time references:

1. **System Time** (`time.time()`): When events occur in real-world
2. **Video Time**: Seconds from recording start (T=0)

**Conversion Formula:**
```
Video Time = Event System Time - Recording Start Time
```

### Event Detection

The GSI server monitors for:
- **Kills**: Detected via `player.match_stats.kills` increment
- **Round Changes**: `round.phase` transitions (live, over, freezetime)
- **Context**: Weapon, headshot status, health, round number

### AI Highlight Criteria

The AI Director prioritizes:
1. Multi-kills (2K, 3K, 4K, ACE)
2. Clutch situations (1vX)
3. Headshot kills
4. High-skill plays
5. Low health survival

**Clip Duration**: 8-15 seconds (optimal for TikTok)

### Video Processing

FFmpeg filter graph:
```
Background: Scale → Crop → Blur (boxblur=20:5)
Foreground: Scale to 1080px width → Center overlay
```

## 🐛 Troubleshooting

### OBS won't connect
- Ensure OBS is running
- Check WebSocket is enabled (Tools → WebSocket Server Settings)
- Verify port and password in config

### No events logged
- Verify `gamestate_integration_highlights.cfg` is in correct CS2 directory
- Check GSI server is running (should show "listening on port 3000")
- Launch CS2 and check console for GSI connection messages

### FFmpeg errors
- Ensure FFmpeg is installed and in PATH: `ffmpeg -version`
- Check source video path is correct
- Try `use_gpu: False` if NVENC issues occur

### AI returns no highlights
- Check `match_log.json` contains kill events
- Lower `min_priority` threshold (try 4 or 5)
- Verify Google API key is valid and has quota remaining
- Get free key at: https://makersuite.google.com/app/apikey

## 📝 License

This project is provided as-is for educational purposes.

## 🙏 Credits

Built with:
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py)
- [Google Gemini API](https://ai.google.dev/) - FREE tier available!
- [FFmpeg](https://ffmpeg.org/)
