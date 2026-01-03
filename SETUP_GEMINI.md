# 🆓 How to Get a Gemini API Key (FREE!)

> 📖 **Questo documento è stato spostato:** [docs/i18n/SETUP_GEMINI.it.md](docs/i18n/SETUP_GEMINI.it.md)
>
> 📖 **English version below**

---

## Why Gemini?

Google Gemini offers a **generous free tier** with no credit card required:
- ✅ **Gemini 2.5 Flash**: 15 requests per minute (RPM) FREE
- ✅ **1500 requests per day** for free
- ✅ No credit card required
- ✅ Perfect for creating highlights from your CS2 matches!

## 📝 Getting an API Key (2 minutes)

### 1. Go to Google AI Studio
Open: **https://aistudio.google.com/app/apikey**

### 2. Sign in with your Google Account
Use your regular Gmail account (nothing special needed)

### 3. Create an API Key
1. Click **"Create API Key"**
2. Choose a Google Cloud project (or create a new one - it's free)
3. Click **"Create API key in new project"**
4. Copy the key that appears (e.g., `AIzaSyC...`)

### 4. Save the Key as Environment Variable

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "AIzaSyC-your-key-here"
```

**Make it permanent (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'AIzaSyC-your-key-here', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="AIzaSyC-your-key-here"
```

**Make it permanent (Linux/Mac):**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GOOGLE_API_KEY="AIzaSyC-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## ✅ Verify Installation

Test if it works:
```bash
python examples/test_gemini_api.py
```

You should see: `✅ GEMINI WORKS PERFECTLY!`

## 🎮 Use the System

Once the key is configured, use the system normally:

```bash
# Phase 1: Live Recording
python main.py live

# Phase 2: Create Highlights (automatically uses GOOGLE_API_KEY)
python main.py process "C:\Videos\cs2_match.mp4"
```

## 📊 Free Tier Limits

| Model | RPM (requests/min) | RPD (requests/day) |
|-------|--------------------|--------------------|
| Gemini 2.5 Flash | 15 | 1500 |
| Gemini 2.5 Pro | 2 | 50 |

**For this project** we use **Gemini 2.5 Flash** which is:
- ⚡ Very fast
- 💰 Completely free
- 🎯 Perfect for analyzing game events

Even with 30 rounds to analyze, you only use ~30 requests = **50 matches per day FREE!**

## 🔗 Useful Links

- **Get API Key**: https://aistudio.google.com/app/apikey
- **Gemini Documentation**: https://ai.google.dev/
- **Pricing**: https://ai.google.dev/pricing

## ❓ Common Issues

### "API key not valid"
- Make sure you copied the entire key
- Restart your terminal after setting the environment variable

### "Quota exceeded"
- You've reached the daily limit (1500 requests)
- Wait until tomorrow or reduce the number of rounds to analyze

### "API not enabled"
- Go to Google Cloud Console
- Enable "Generative Language API"
