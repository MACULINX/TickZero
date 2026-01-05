# TickZero

**TickZero: AI-driven highlight extraction for CS2. Transform your Counter-Strike 2 gameplay into viral TikTok/Reels clips automatically using FREE AI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **Read this in other languages:** [Italiano](docs/i18n/README.it.md) · [Español](docs/i18n/README.es.md) · [Français](docs/i18n/README.fr.md) · [Deutsch](docs/i18n/README.de.md) · [Русский](docs/i18n/README.ru.md) · [简体中文](docs/i18n/README.zh.md)

## 🎯 Features

- **🎮 Live Event Logging** - Captures kills, headshots, and round events in real-time via CS2 Game State Integration
- **⏱️ OBS Synchronization** - Precise timestamp alignment between game events and video recording
- **🤖 AI-Powered Analysis** - Uses Google Gemini (FREE tier) to identify highlight-worthy moments
- **✂️ Automatic Video Editing** - FFmpeg-based conversion to vertical format (9:16) with blurred background
- **🎮 Multi-GPU Support** - Automatic detection and optimization for NVIDIA, AMD, and Intel GPUs
- **🔄 Continuous Recording** - Record multiple matches with automatic processing between games
- **⚡ Hardware Acceleration** - Smart fallback: NVIDIA NVENC → AMD AMF → Intel QSV → CPU

## 📋 Requirements

### Software
- **Python** 3.10 or higher
- **OBS Studio** with WebSocket plugin enabled
- **FFmpeg** (hardware encoding support optional)
- **Counter-Strike 2**
- **Google API Key** for Gemini (FREE tier available - no credit card required!)

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. Configure OBS WebSocket

1. Open **OBS Studio**
2. Go to **Tools → WebSocket Server Settings**
3. Enable WebSocket server
4. Note the port (default: `4455`) and password (if set)
5. Update `config` in `main.py` if needed

### 3. Enable CS2 Game State Integration

Copy `gamestate_integration_highlights.cfg` to your CS2 config folder:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. Get Google Gemini API Key (FREE!)

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your key (starts with `AIzaSy...`)
5. Set it as environment variable:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "your-api-key-here"

# Make it permanent:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'your-api-key-here', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your-api-key-here"

# Make it permanent (add to ~/.bashrc or ~/.zshrc):
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **Note:** Gemini 2.5 Flash is FREE with 1500 requests/day. That's enough for ~50 matches per day!

## 📖 Usage

The pipeline works in **two phases**:

### Phase 1: Live Logging (During Match)

Run this **BEFORE** starting your CS2 match:

```bash
python main.py live
```

**What happens:**
1. ✅ Connects to OBS WebSocket
2. ✅ Starts GSI server on port 3000
3. ⏳ **Waits for match to start**
4. ✅ **Automatically starts recording** when the first round goes live
5. ✅ Logs all game events with precise video timestamps
6. ✅ **Automatically stops recording** when match ends (in continuous mode)

> **Note:** With `auto_recording: True` (default), recording starts automatically when the match begins, not when you run the script. This ensures you only record actual gameplay, not warmup or menu time. The system detects match start when the first round transitions to "live" phase.

Play your match normally. The system will automatically handle recording.

**Manual Stop:** Press `Ctrl+C` to stop logging (if not using continuous mode).

Events are saved to `match_log.json`.

### Phase 2: Post-Processing (After Match)

Run this **AFTER** the match to create highlight clips:

```bash
python main.py process <path_to_recording.mp4> [api_key] [min_priority]
```

**Example:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**Parameters:**
- `<path_to_recording.mp4>` - Path to your OBS recording (required)
- `[api_key]` - Google API key (optional if `GOOGLE_API_KEY` env var is set)
- `[min_priority]` - Minimum clip priority 1-10 (default: 6)

**What happens:**
1. 🤖 AI analyzes `match_log.json`
2. 🎯 Identifies highlight moments (multi-kills, clutches, headshots)
3. ✂️ Creates vertical video clips in `highlights/` directory

## 🎬 Output Format

**Vertical Video Specifications:**
- **Resolution:** 1080×1920 (9:16 aspect ratio)
- **Format:** MP4 (H.264)
- **Audio:** AAC stereo
- **Visual Style:** Blurred background + centered gameplay

**File Naming Convention:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🎯 How It Works

### Timestamp Synchronization

The system maintains two time references:

1. **System Time** (`time.time()`) - When events occur in real-world
2. **Video Time** - Seconds from recording start (T=0)

**Conversion Formula:**
```
Video Time = Event System Time - Recording Start Time
```

### Event Detection

The GSI server monitors:
- **Kills** - Detected via `player.match_stats.kills` increment **for the main player only**
- **Round Changes** - `round.phase` transitions (live, over, freezetime)
- **Context** - Weapon used, headshot status, player health, round number

> **Note:** When you die and spectate teammates, the system automatically ignores their kills. Only kills performed by the player who launched the program are logged, ensuring accurate personal highlight tracking.

### AI Highlight Criteria

The AI Director (powered by Google Gemini) prioritizes:

1. 🔥 **Multi-kills** (2K, 3K, 4K, ACE) - More kills = Higher priority
2. 💪 **Clutch situations** (1v2, 1v3, 1v4, 1v5) - Especially if won
3. 🎯 **Headshot kills** - One-taps get extra points
4. ⚡ **High-skill plays** - Quick reactions, difficult shots
5. ❤️ **Low health clutches** - Surviving with <20 HP

**Clip Duration:** 8-15 seconds (optimal for TikTok/Reels)

### Video Processing Pipeline

FFmpeg applies this filter graph:

```
Background: Scale → Crop to 9:16 → Blur (boxblur=20:5)
Foreground: Scale to 1080px width → Center overlay
```

## 🔧 Configuration

Edit the `config` dictionary in `main.py`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # OBS WebSocket port
    'obs_password': '',            # OBS WebSocket password (if set)
    'gsi_port': 3000,              # GSI server port
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True,               # Enable GPU acceleration
    'auto_recording': True,        # Auto-start/stop recording based on match detection
    'continuous_mode': True,       # Auto-process after each match
    'auto_process': True,          # Enable automatic processing
    'auto_min_priority': 6         # Minimum clip priority (1-10)
}
```

### GPU Acceleration

TickZero automatically detects and uses the best available GPU encoder:

1. **NVIDIA NVENC** (h264_nvenc) - Requires NVIDIA GPU with drivers
2. **AMD AMF** (h264_amf) - Requires AMD Radeon GPU
3. **Intel QuickSync** (h264_qsv) - Requires Intel CPU with integrated graphics
4. **CPU Fallback** (libx264) - Works on any system

The system automatically tests each encoder and uses the first working option.

### Continuous Recording Mode

When `continuous_mode: True`, TickZero:
- Detects match end automatically (via "gameover" event)
- Processes highlights in background
- Continues recording for the next match
- No need to restart between matches!

**Perfect for:** Multi-match gaming sessions, competitive play, streaming

## 🐛 Troubleshooting

### OBS Connection Issues
- ✅ Ensure OBS Studio is running
- ✅ Check WebSocket is enabled: **Tools → WebSocket Server Settings**
- ✅ Verify port and password match your config

### No Events Being Logged
- ✅ Verify `gamestate_integration_highlights.cfg` is in the correct CS2 directory
- ✅ Check GSI server is running (should show "Listening on port 3000")
- ✅ Launch CS2 and check console for GSI connection messages

### FFmpeg Errors
- ✅ Ensure FFmpeg is installed: `ffmpeg -version`
- ✅ Verify source video path is correct
- ✅ Try setting `use_gpu: False` if you encounter NVENC errors

### AI Returns No Highlights
- ✅ Check `match_log.json` contains kill events
- ✅ Lower `min_priority` threshold (try 4 or 5)
- ✅ Verify Google API key is valid: run `python examples/test_gemini_api.py`
- ✅ Check you haven't exceeded daily quota (1500 requests)

### Teammate Kills Being Logged
- ✅ Ensure you're using the latest version of `gsi_server.py` with SteamID filtering
- ✅ Check console output shows "👤 Main player locked" with your name at match start
- ✅ Run `python debug_gsi_payload.py` to verify SteamID consistency in GSI payloads

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

**Development:**
```bash
# Fork the repository
git clone https://github.com/yourusername/cs2-highlights-pipeline.git
cd cs2-highlights-pipeline

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m "Add amazing feature"

# Push to your fork
git push origin feature/amazing-feature

# Open a Pull Request
```

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Summary:** You can freely use, modify, and distribute this code, but you must include the original copyright notice and cannot hold the authors liable.

## 🙏 Acknowledgments

### Built With
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - OBS WebSocket Python client
- [Google Gemini API](https://ai.google.dev/) - AI-powered highlight analysis
- [FFmpeg](https://ffmpeg.org/) - Video processing engine

### AI Assistance
Parts of this project's codebase were created with the assistance of AI language models (Google Gemini, Claude) to accelerate development and improve code quality. All AI-generated code has been reviewed, tested, and adapted for this specific use case.

### Community
Special thanks to the Counter-Strike community and content creators who inspired this project.

## 📞 Support

- 🐛 **Bug Reports:** [Open an issue](https://github.com/MACULINX/TickZero/issues)
- 💡 **Feature Requests:** [Start a discussion](https://github.com/MACULINX/TickZero/discussions)
- 📧 **Contact:** [@MACULINX](https://github.com/MACULINX)

---

**Made with ❤️ by gamers, for gamers.**

**Star ⭐ this repo if you found it useful!**
