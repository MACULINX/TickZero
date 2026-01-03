# CS2 Highlight Pipeline - Guida Rapida

## ✅ Setup Completato

Virtual environment creata e dipendenze installate!

## 🔑 Prossimo Passo: Configura API Key Gemini

### Opzione 1: Ottieni Chiave API (GRATIS - 2 minuti)

1. Vai su: **https://aistudio.google.com/app/apikey**
2. Accedi con Google
3. Clicca "Create API Key"
4. Copia la chiave (es: `AIzaSyC...`)

### Opzione 2: Configura la Chiave

**Permanente (consigliato):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'AIzaSyC-tua-chiave-qui', 'User')
```

**Temporanea (solo sessione corrente):**
```powershell
$env:GOOGLE_API_KEY = "AIzaSyC-tua-chiave-qui"
```

### Opzione 3: Testa Gemini

```powershell
.\venv\Scripts\Activate.ps1
python examples\test_gemini_api.py
```

Dovresti vedere: `✅ GEMINI FUNZIONA PERFETTAMENTE!`

## 🎮 Come Usare il Sistema

### Fase 1: Registra il Match
```powershell
.\venv\Scripts\Activate.ps1
python main.py live
```

Avvia PRIMA di giocare CS2. Logga tutti gli eventi.
Premi `Ctrl+C` quando finisci.

### Fase 2: Crea Highlights
```powershell
.\venv\Scripts\Activate.ps1
python main.py process "percorso\video.mp4"
```

Crea clip verticali in `highlights/`!

## 📋 Checklist Setup

- [x] Python 3.10+ installato
- [x] Virtual environment creata (`venv/`)
- [x] Dipendenze installate (`google-genai`, `obs-websocket-py`)
- [ ] API key Gemini configurata
- [ ] OBS WebSocket abilitato
- [ ] CS2 GSI config copiato

**Prossimo passo: Ottieni l'API key e testa!**
