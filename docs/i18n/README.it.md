# TickZero

**TickZero: Estrazione highlight guidata da AI per CS2. Trasforma automaticamente il tuo gameplay di Counter-Strike 2 in clip virali per TikTok/Reels usando l'AI GRATUITA.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **Leggi in altre lingue:** [English](../../README.md)

## 🎯 Funzionalità

- **🎮 Logging Live degli Eventi** - Cattura kill, headshot ed eventi di round in tempo reale tramite Game State Integration di CS2
- **⏱️ Sincronizzazione OBS** - Allineamento preciso del timestamp tra eventi di gioco e registrazione video
- **🤖 Analisi Powered by AI** - Usa Google Gemini (tier GRATUITO) per identificare momenti degni di highlight
- **✂️ Editing Video Automatico** - Conversione basata su FFmpeg in formato verticale (9:16) con sfondo sfocato
- **⚡ Accelerazione Hardware** - Supporta NVIDIA NVENC con fallback automatico su CPU

## 📋 Requisiti

### Software
- **Python** 3.10 o superiore
- **OBS Studio** con plugin WebSocket abilitato
- **FFmpeg** (supporto encoding hardware opzionale)
- **Counter-Strike 2**
- **Chiave API Google** per Gemini (tier GRATUITO disponibile - nessuna carta di credito richiesta!)

### Dipendenze Python
```bash
pip install -r requirements.txt
```

**Dipendenze:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 Guida Rapida

### 1. Clona e Installa

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. Configura WebSocket di OBS

1. Apri **OBS Studio**
2. Vai su **Strumenti → Impostazioni Server WebSocket**
3. Abilita il server WebSocket
4. Annota la porta (default: `4455`) e la password (se impostata)
5. Aggiorna `config` in `main.py` se necessario

### 3. Abilita Game State Integration di CS2

Copia `gamestate_integration_highlights.cfg` nella cartella config di CS2:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. Ottieni la Chiave API di Google Gemini (GRATIS!)

1. Visita [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Accedi con il tuo account Google
3. Clicca su **"Create API Key"**
4. Copia la tua chiave (inizia con `AIzaSy...`)
5. Impostala come variabile d'ambiente:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "tua-chiave-api-qui"

# Rendila permanente:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'tua-chiave-api-qui', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="tua-chiave-api-qui"

# Rendila permanente (aggiungi a ~/.bashrc o ~/.zshrc):
echo 'export GOOGLE_API_KEY="tua-chiave-api-qui"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **Nota:** Gemini 2.5 Flash è GRATUITO con 1500 richieste/giorno. Abbastanza per ~50 partite al giorno!

## 📖 Utilizzo

La pipeline funziona in **due fasi**:

### Fase 1: Logging Live (Durante la Partita)

Esegui questo **PRIMA** di iniziare la tua partita CS2:

```bash
python main.py live
```

**Cosa succede:**
1. ✅ Si connette a OBS WebSocket
2. ✅ Avvia la registrazione automaticamente
3. ✅ Avvia il server GSI sulla porta 3000
4. ✅ Logga tutti gli eventi di gioco con timestamp video precisi

Gioca la tua partita normalmente. Quando finisci, premi `Ctrl+C` per fermare il logging.

Gli eventi vengono salvati in `match_log.json`.

### Fase 2: Post-Elaborazione (Dopo la Partita)

Esegui questo **DOPO** la partita per creare le clip degli highlight:

```bash
python main.py process <percorso_registrazione.mp4> [api_key] [priorita_minima]
```

**Esempio:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**Parametri:**
- `<percorso_registrazione.mp4>` - Percorso della registrazione OBS (obbligatorio)
- `[api_key]` - Chiave API Google (opzionale se la variabile d'ambiente `GOOGLE_API_KEY` è impostata)
- `[priorita_minima]` - Priorità minima clip 1-10 (default: 6)

**Cosa succede:**
1. 🤖 L'AI analizza `match_log.json`
2. 🎯 Identifica momenti degni di highlight (multi-kill, clutch, headshot)
3. ✂️ Crea clip video verticali nella cartella `highlights/`

## 🎬 Formato Output

**Specifiche Video Verticale:**
- **Risoluzione:** 1080×1920 (aspect ratio 9:16)
- **Formato:** MP4 (H.264)
- **Audio:** AAC stereo
- **Stile Visivo:** Sfondo sfocato + gameplay centrato

**Convenzione Nomi File:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🎯 Come Funziona

### Sincronizzazione Timestamp

Il sistema mantiene due riferimenti temporali:

1. **System Time** (`time.time()`) - Quando gli eventi avvengono nel mondo reale
2. **Video Time** - Secondi dall'inizio della registrazione (T=0)

**Formula di Conversione:**
```
Video Time = Event System Time - Recording Start Time
```

### Rilevamento Eventi

Il server GSI monitora:
- **Kill** - Rilevate tramite incremento di `player.match_stats.kills`
- **Cambi Round** - Transizioni di `round.phase` (live, over, freezetime)
- **Contesto** - Arma usata, stato headshot, salute giocatore, numero round

### Criteri Highlight AI

L'AI Director (powered by Google Gemini) dà priorità a:

1. 🔥 **Multi-kill** (2K, 3K, 4K, ACE) - Più kill = Priorità maggiore
2. 💪 **Situazioni Clutch** (1v2, 1v3, 1v4, 1v5) - Specialmente se vinte
3. 🎯 **Kill Headshot** - I one-tap ottengono punti extra
4. ⚡ **Play ad Alta Skill** - Reazioni rapide, colpi difficili
5. ❤️ **Clutch a Vita Bassa** - Sopravvivere con <20 HP

**Durata Clip:** 8-15 secondi (ottimale per TikTok/Reels)

### Pipeline di Elaborazione Video

FFmpeg applica questo grafo di filtri:

```
Background: Scale → Crop a 9:16 → Blur (boxblur=20:5)
Foreground: Scale a larghezza 1080px → Overlay centrato
```

## 🔧 Configurazione

Modifica il dizionario `config` in `main.py`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # Porta OBS WebSocket
    'obs_password': '',            # Password OBS WebSocket (se impostata)
    'gsi_port': 3000,              # Porta server GSI
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True                # Usa NVENC se disponibile
}
```

## 🐛 Risoluzione Problemi

### Problemi di Connessione OBS
- ✅ Assicurati che OBS Studio sia in esecuzione
- ✅ Verifica che WebSocket sia abilitato: **Strumenti → Impostazioni Server WebSocket**
- ✅ Verifica che porta e password corrispondano alla tua config

### Nessun Evento Viene Loggato
- ✅ Verifica che `gamestate_integration_highlights.cfg` sia nella cartella CS2 corretta
- ✅ Controlla che il server GSI sia in esecuzione (dovrebbe mostrare "Listening on port 3000")
- ✅ Lancia CS2 e controlla la console per messaggi di connessione GSI

### Errori FFmpeg
- ✅ Assicurati che FFmpeg sia installato: `ffmpeg -version`
- ✅ Verifica che il percorso del video sorgente sia corretto
- ✅ Prova a impostare `use_gpu: False` se incontri errori NVENC

### L'AI Non Restituisce Highlight
- ✅ Controlla che `match_log.json` contenga eventi di kill
- ✅ Abbassa la soglia `min_priority` (prova 4 o 5)
- ✅ Verifica che la chiave API Google sia valida: esegui `python examples/test_gemini_api.py`
- ✅ Controlla di non aver superato la quota giornaliera (1500 richieste)

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di inviare una Pull Request. Per modifiche importanti, apri prima un issue per discutere cosa vorresti cambiare.

**Sviluppo:**
```bash
# Forka il repository
git clone https://github.com/yourusername/cs2-highlights-pipeline.git
cd cs2-highlights-pipeline

# Crea un branch per la feature
git checkout -b feature/funzionalita-fantastica

# Fai le tue modifiche e committa
git commit -m "Aggiungi funzionalità fantastica"

# Pusha al tuo fork
git push origin feature/funzionalita-fantastica

# Apri una Pull Request
```

## 📝 Licenza

Questo progetto è rilasciato sotto **Licenza MIT** - vedi il file [LICENSE](../../LICENSE) per i dettagli.

**Riepilogo:** Puoi liberamente usare, modificare e distribuire questo codice, ma devi includere l'avviso di copyright originale e non puoi ritenere responsabili gli autori.

## 🙏 Riconoscimenti

### Costruito Con
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - Client Python per OBS WebSocket
- [Google Gemini API](https://ai.google.dev/) - Analisi highlight powered by AI
- [FFmpeg](https://ffmpeg.org/) - Motore di elaborazione video

### Assistenza AI
Parti del codice di questo progetto sono state create con l'assistenza di modelli di linguaggio AI (Google Gemini, Claude) per accelerare lo sviluppo e migliorare la qualità del codice. Tutto il codice generato dall'AI è stato rivisto, testato e adattato per questo caso d'uso specifico.

### Community
Ringraziamenti speciali alla comunità di Counter-Strike e ai content creator che hanno ispirato questo progetto.

## 📞 Supporto

- 🐛 **Segnalazione Bug:** [Apri un issue](https://github.com/MACULINX/TickZero/issues)
- 💡 **Richieste Funzionalità:** [Avvia una discussione](https://github.com/MACULINX/TickZero/discussions)
- 📧 **Contatti:** [@MACULINX](https://github.com/MACULINX)

---

**Fatto con ❤️ da giocatori, per giocatori.**

**Metti una stella ⭐ a questo repo se l'hai trovato utile!**
