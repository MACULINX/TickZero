# TickZero

**TickZero: KI-gesteuerte Highlight-Extraktion für CS2. Verwandeln Sie Ihr Counter-Strike 2 Gameplay automatisch in virale TikTok/Reels-Clips mit KOSTENLOSER KI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **In anderen Sprachen lesen:** [English](../../README.md) · [Italiano](README.it.md) · [Español](README.es.md) · [Français](README.fr.md) · [Русский](README.ru.md) · [简体中文](README.zh.md)

## 🎯 Features

- **🎮 Live-Event-Logging** - Erfasst Kills, Headshots und Rundenevents in Echtzeit über CS2 Game State Integration
- **⏱️ OBS-Synchronisation** - Präzise Zeitstempel-Ausrichtung zwischen Spielereignissen und Videoaufzeichnung
- **🤖 KI-gestützte Analyse** - Nutzt Google Gemini (KOSTENLOS) zur Identifizierung highlight-würdiger Momente
- **✂️ Automatische Videobearbeitung** - FFmpeg-basierte Konvertierung ins vertikale Format (9:16) mit verschwommenem Hintergrund
- **⚡ Hardware-Beschleunigung** - Unterstützt NVIDIA NVENC mit automatischem CPU-Fallback

## 📋 Voraussetzungen

### Software
- **Python** 3.10 oder höher
- **OBS Studio** mit aktiviertem WebSocket-Plugin
- **FFmpeg** (Hardware-Encoding-Unterstützung optional)
- **Counter-Strike 2**
- **Google API-Schlüssel** für Gemini (KOSTENLOS verfügbar - keine Kreditkarte erforderlich!)

### Python-Abhängigkeiten
```bash
pip install -r requirements.txt
```

**Abhängigkeiten:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 Schnellstart

### 1. Klonen und Installieren

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. OBS WebSocket Konfigurieren

1. **OBS Studio** öffnen
2. Zu **Tools → WebSocket Server-Einstellungen** gehen
3. WebSocket-Server aktivieren
4. Port notieren (Standard: `4455`) und Passwort (falls gesetzt)
5. `config` in `main.py` aktualisieren:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # OBS WebSocket Port
    'obs_password': '',            # OBS WebSocket Passwort
    'gsi_port': 3000,              # GSI Server Port
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True,               # GPU-Beschleunigung aktivieren
    'continuous_mode': True,       # Auto-Verarbeitung nach jedem Match
    'auto_process': True,          # Automatische Verarbeitung aktivieren
    'auto_min_priority': 6         # Minimale Priorität (1-10)
}
```

### GPU-Beschleunigung

TickZero erkennt und nutzt automatisch den besten verfügbaren GPU-Encoder:

1. **NVIDIA NVENC** (h264_nvenc) - Erfordert NVIDIA GPU mit Treibern
2. **AMD AMF** (h264_amf) - Erfordert AMD Radeon GPU
3. **Intel QuickSync** (h264_qsv) - Erfordert Intel CPU mit integrierter Grafik
4. **CPU Fallback** (libx264) - Funktioniert auf jedem System

### Kontinuierlicher Aufnahmemodus

Mit `continuous_mode: True`, TickZero:
- Erkennt automatisch das Spielende (Ereignis "gameover")
- Verarbeitet Highlights im Hintergrund
- Setzt die Aufnahme für das nächste Match fort
- Kein Neustart zwischen Matches erforderlich!

### 3. CS2 Game State Integration Aktivieren

`gamestate_integration_highlights.cfg` in Ihren CS2-Konfigurationsordner kopieren:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. Google Gemini API-Schlüssel Erhalten (KOSTENLOS!)

1. [Google AI Studio](https://aistudio.google.com/app/apikey) besuchen
2. Mit Ihrem Google-Konto anmelden
3. Auf **"Create API Key"** klicken
4. Ihren Schlüssel kopieren (beginnt mit `AIzaSy...`)
5. Als Umgebungsvariable festlegen:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "ihr-api-schlüssel-hier"

# Permanent machen:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'ihr-api-schlüssel-hier', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="ihr-api-schlüssel-hier"

# Permanent machen (zu ~/.bashrc oder ~/.zshrc hinzufügen):
echo 'export GOOGLE_API_KEY="ihr-api-schlüssel-hier"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **Hinweis:** Gemini 2.5 Flash ist KOSTENLOS mit 1500 Anfragen/Tag. Das reicht für ~50 Matches pro Tag!

## 📖 Verwendung

Die Pipeline arbeitet in **zwei Phasen**:

### Phase 1: Live-Logging (Während des Matches)

Dies **VOR** Beginn Ihres CS2-Matches ausführen:

```bash
python main.py live
```

**Was passiert:**
1. ✅ Verbindet sich mit OBS WebSocket
2. ✅ Startet Aufnahme automatisch
3. ✅ Startet GSI-Server auf Port 3000
4. ✅ Protokolliert alle Spielereignisse mit präzisen Video-Zeitstempeln

Spielen Sie Ihr Match normal. Wenn Sie fertig sind, drücken Sie `Ctrl+C`, um die Aufzeichnung zu stoppen.

Ereignisse werden in `match_log.json` gespeichert.

### Phase 2: Nachbearbeitung (Nach dem Match)

Dies **NACH** dem Match ausführen, um Highlight-Clips zu erstellen:

```bash
python main.py process <pfad_zur_aufnahme.mp4> [api_schlüssel] [min_priorität]
```

**Beispiel:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**Parameter:**
- `<pfad_zur_aufnahme.mp4>` - Pfad zu Ihrer OBS-Aufnahme (erforderlich)
- `[api_schlüssel]` - Google API-Schlüssel (optional, wenn `GOOGLE_API_KEY` Umgebungsvariable gesetzt ist)
- `[min_priorität]` - Minimale Clip-Priorität 1-10 (Standard: 6)

**Was passiert:**
1. 🤖 KI analysiert `match_log.json`
2. 🎯 Identifiziert Highlight-Momente (Multi-Kills, Clutches, Headshots)
3. ✂️ Erstellt vertikale Videoclips im Verzeichnis `highlights/`

## 🎬 Ausgabeformat

**Vertikale Video-Spezifikationen:**
- **Auflösung:** 1080×1920 (9:16 Seitenverhältnis)
- **Format:** MP4 (H.264)
- **Audio:** AAC Stereo
- **Visueller Stil:** Verschwommener Hintergrund + zentriertes Gameplay

**Dateinamenskonvention:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🐛 Fehlerbehebung

### OBS Verbindungsprobleme
- ✅ Stellen Sie sicher, dass OBS Studio läuft
- ✅ Prüfen Sie, ob WebSocket aktiviert ist: **Tools → WebSocket Server-Einstellungen**
- ✅ Überprüfen Sie, ob Port und Passwort mit Ihrer Konfiguration übereinstimmen

### Keine Ereignisse werden protokolliert
- ✅ Überprüfen Sie, ob `gamestate_integration_highlights.cfg` im richtigen CS2-Ordner liegt
- ✅ Prüfen Sie, ob der GSI-Server läuft (sollte "Listening on port 3000" anzeigen)
- ✅ Starten Sie CS2 und prüfen Sie die Konsole auf GSI-Verbindungsmeldungen

### FFmpeg Fehler
- ✅ Stellen Sie sicher, dass FFmpeg installiert ist: `ffmpeg -version`
- ✅ Überprüfen Sie, ob der Quellvidepfad korrekt ist
- ✅ Versuchen Sie `use_gpu: False` zu setzen, wenn NVENC-Fehler auftreten

### KI liefert keine Highlights
- ✅ Überprüfen Sie, ob `match_log.json` Kill-Ereignisse enthält
- ✅ Senken Sie den `min_priority` Schwellenwert (versuchen Sie 4 oder 5)
- ✅ Überprüfen Sie, ob Ihr Google API-Schlüssel gültig ist: `python examples/test_gemini_api.py` ausführen
- ✅ Prüfen Sie, ob das tägliche Kontingent (1500 Anfragen) überschritten wurde

## 🤝 Mitwirken

Beiträge sind willkommen! Fühlen Sie sich frei, einen Pull Request einzureichen. Für größere Änderungen öffnen Sie bitte zuerst ein Issue, um zu besprechen, was Sie ändern möchten.

Siehe [CONTRIBUTING.md](../../CONTRIBUTING.md) für Details.

## 📝 Lizenz

Dieses Projekt ist lizenziert unter der **MIT-Lizenz** - siehe die Datei [LICENSE](../../LICENSE) für Details.

**Zusammenfassung:** Sie können diesen Code frei verwenden, modifizieren und verteilen, müssen aber den ursprünglichen Copyright-Hinweis einschließen und können die Autoren nicht haftbar machen.

## 🙏 Danksagungen

### Erstellt Mit
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - Python-Client für OBS WebSocket
- [Google Gemini API](https://ai.google.dev/) - KI-gestützte Highlight-Analyse
- [FFmpeg](https://ffmpeg.org/) - Video-Verarbeitungs-Engine

### KI-Unterstützung
Teile der Codebasis dieses Projekts wurden mit Unterstützung von KI-Sprachmodellen (Google Gemini, Claude) erstellt, um die Entwicklung zu beschleunigen und die Codequalität zu verbessern. Jeglicher KI-generierter Code wurde überprüft, getestet und für diesen spezifischen Anwendungsfall angepasst.

---

**Mit ❤️ von Gamern für Gamer gemacht.**

**Geben Sie diesem Repo einen Stern ⭐, wenn Sie es nützlich fanden!**
