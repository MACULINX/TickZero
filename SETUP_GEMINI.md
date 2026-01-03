# 🆓 Come Ottenere la Chiave API di Gemini (GRATIS!)

## Perché Gemini?

Google Gemini offre un **piano gratuito generoso** senza carta di credito richiesta:
- ✅ **Gemini 1.5 Flash**: 15 richieste al minuto (RPM) GRATIS
- ✅ **1500 richieste al giorno** gratuite
- ✅ Nessuna carta di credito richiesta
- ✅ Perfetto per creare highlight dai tuoi match CS2!

## 📝 Ottenere la Chiave API (2 minuti)

### 1. Vai su Google AI Studio
Apri: **https://makersuite.google.com/app/apikey**

### 2. Accedi con il tuo Account Google
Usa il tuo account Gmail normale (non serve niente di speciale)

### 3. Crea una Chiave API
1. Clicca su **"Create API Key"** (o "Ottieni chiave API")
2. Scegli un progetto Google Cloud (o creane uno nuovo - è gratis)
3. Clicca su **"Create API key in new project"**
4. Copia la chiave che appare (es: `AIzaSyC...`)

### 4. Salva la Chiave come Variabile d'Ambiente

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "AIzaSyC-tua-chiave-qui"
```

**Per renderla permanente (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'AIzaSyC-tua-chiave-qui', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="AIzaSyC-tua-chiave-qui"
```

**Per renderla permanente (Linux/Mac):**
Aggiungi al file `~/.bashrc` o `~/.zshrc`:
```bash
echo 'export GOOGLE_API_KEY="AIzaSyC-tua-chiave-qui"' >> ~/.bashrc
source ~/.bashrc
```

## ✅ Verifica Installazione

Testa se funziona:
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Test")
print("✓ Gemini funziona!")
```

## 🎮 Usa il Sistema

Una volta configurata la chiave, usa il sistema normalmente:

```bash
# Fase 1: Registrazione Live
python main.py live

# Fase 2: Crea Highlights (usa automaticamente GOOGLE_API_KEY)
python main.py process "C:\Videos\cs2_match.mp4"
```

## 📊 Limiti del Piano Gratuito

| Modello | RPM (richieste/min) | RPD (richieste/giorno) |
|---------|---------------------|------------------------|
| Gemini 1.5 Flash | 15 | 1500 |
| Gemini 1.5 Pro | 2 | 50 |

**Per questo progetto** usiamo **Gemini 1.5 Flash** che è:
- ⚡ Velocissimo
- 💰 Completamente gratuito
- 🎯 Perfetto per analizzare eventi di gioco

Anche con 30 round da analizzare, usi solo ~30 richieste = **50 partite al giorno GRATIS!**

## 🔗 Link Utili

- **Ottieni Chiave API**: https://makersuite.google.com/app/apikey
- **Documentazione Gemini**: https://ai.google.dev/
- **Pricing**: https://ai.google.dev/pricing

## ❓ Problemi Comuni

### "API key not valid"
- Verifica di aver copiato tutta la chiave
- Riavvia il terminale dopo aver impostato la variabile d'ambiente

### "Quota exceeded"
- Hai raggiunto il limite giornaliero (1500 richieste)
- Aspetta domani o riduci il numero di round da analizzare

### "API not enabled"
- Vai su Google Cloud Console
- Abilita "Generative Language API"
