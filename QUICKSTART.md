# CS2 Highlight Pipeline - Quick Start

> 📖 **Questo documento è stato spostato:** [docs/i18n/QUICKSTART.it.md](docs/i18n/QUICKSTART.it.md)
>
> 📖 **English version:** See [README.md](README.md)

---

## ✅ Setup Complete

Virtual environment created and dependencies installed via Poetry!

## 🔑 Next Step: Configure Gemini API Key

### Option 1: Get API Key (FREE - 2 minutes)

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click "Create API Key"
4. Copy your key (e.g., `AIzaSyC...`)

### Option 2: Configure the Key

**Permanent (recommended):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'AIzaSyC-your-key-here', 'User')
```

**Temporary (current session only):**
```powershell
$env:GOOGLE_API_KEY = "AIzaSyC-your-key-here"
```

### Option 3: Test Gemini

```powershell
poetry run python examples/test_gemini_api.py
```

You should see: `✅ GEMINI WORKS PERFECTLY!`

## 🎮 How to Use the System

### Phase 1: Record the Match
```powershell
poetry run python -m tickzero.launcher record
```

Start BEFORE playing CS2. Logs all events.
Press `Ctrl+C` when finished.

### Phase 2: Create Highlights
```powershell
poetry run python -m tickzero.launcher process --video "path\to\video.mp4" --log "match_log.json"
```

Creates vertical clips in `highlights/`!

## 📋 Setup Checklist

- [x] Python 3.10+ installed
- [x] Poetry installed
- [x] Dependencies installed (`poetry install`)
- [ ] Gemini API key configured
- [ ] OBS WebSocket enabled
- [ ] CS2 GSI config copied

**Next step: Get the API key and test it!**
