# TickZero

**TickZero: Extraction de moments forts guidée par IA pour CS2. Transformez automatiquement votre gameplay Counter-Strike 2 en clips viraux pour TikTok/Reels grâce à l'IA GRATUITE.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 📖 **Lire dans d'autres langues:** [English](../../README.md) · [Italiano](README.it.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [简体中文](README.zh.md)

## 🎯 Fonctionnalités

- **🎮 Enregistrement d'Événements en Direct** - Capture les kills, headshots et événements de round en temps réel via CS2 Game State Integration
- **⏱️ Synchronisation OBS** - Alignement précis des timestamps entre les événements de jeu et l'enregistrement vidéo
- **🤖 Analyse par IA** - Utilise Google Gemini (niveau GRATUIT) pour identifier les moments dignes d'être mis en avant
- **✂️ Montage Vidéo Automatique** - Conversion basée sur FFmpeg au format vertical (9:16) avec arrière-plan flouté
- **⚡ Accélération Matérielle** - Supporte NVIDIA NVENC avec basculement automatique sur CPU

## 📋 Prérequis

### Logiciels
- **Python** 3.10 ou supérieur
- **OBS Studio** avec plugin WebSocket activé
- **FFmpeg** (support d'encodage matériel optionnel)
- **Counter-Strike 2**
- **Clé API Google** pour Gemini (niveau GRATUIT disponible - aucune carte bancaire requise!)

### Dépendances Python
```bash
pip install -r requirements.txt
```

**Dépendances:** `google-genai`, `obs-websocket-py`, `flask`

## 🚀 Guide Rapide

### 1. Cloner et Installer

```bash
git clone https://github.com/MACULINX/TickZero.git
cd TickZero
pip install -r requirements.txt
```

### 2. Configurer WebSocket OBS

1. Ouvrir **OBS Studio**
2. Aller dans **Outils → Paramètres du Serveur WebSocket**
3. Activer le serveur WebSocket
4. Noter le port (par défaut: `4455`) et le mot de passe (si défini)
5. Mettre à jour `config` dans `main.py`:

```python
config = {
    'obs_host': 'localhost',
    'obs_port': 4455,              # Port OBS WebSocket
    'obs_password': '',            # Mot de passe OBS WebSocket
    'gsi_port': 3000,              # Port serveur GSI
    'log_file': 'match_log.json',
    'output_dir': 'highlights',
    'use_gpu': True,               # Activer l'accélération GPU
    'continuous_mode': True,       # Auto-traitement après chaque match
    'auto_process': True,          # Activer le traitement automatique
    'auto_min_priority': 6         # Priorité minimale (1-10)
}
```

### Accélération Matérielle GPU

TickZero détecte et utilise automatiquement le meilleur encodeur GPU disponible:

1. **NVIDIA NVENC** (h264_nvenc) - Nécessite GPU NVIDIA avec pilotes
2. **AMD AMF** (h264_amf) - Nécessite GPU AMD Radeon
3. **Intel QuickSync** (h264_qsv) - Nécessite CPU Intel avec graphismes intégrés
4. **CPU Fallback** (libx264) - Fonctionne sur tous les systèmes

### Mode Enregistrement Continu

Avec `continuous_mode: True`, TickZero:
- Détecte automatiquement la fin du match (événement "gameover")
- Traite les moments forts en arrière-plan
- Continue l'enregistrement pour le match suivant
- Pas besoin de redémarrer entre les matchs !

### 3. Activer l'Intégration d'État de Jeu CS2

Copier `gamestate_integration_highlights.cfg` dans votre dossier de configuration CS2:

```
Windows: C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
Linux:   ~/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/cfg/
```

### 4. Obtenir une Clé API Google Gemini (GRATUIT!)

1. Visiter [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Se connecter avec votre compte Google
3. Cliquer sur **"Create API Key"**
4. Copier votre clé (commence par `AIzaSy...`)
5. La définir comme variable d'environnement:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY = "votre-cle-api-ici"

# Rendre permanent:
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', 'votre-cle-api-ici', 'User')
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="votre-cle-api-ici"

# Rendre permanent (ajouter à ~/.bashrc ou ~/.zshrc):
echo 'export GOOGLE_API_KEY="votre-cle-api-ici"' >> ~/.bashrc
source ~/.bashrc
```

> 💡 **Note:** Gemini 2.5 Flash est GRATUIT avec 1500 requêtes/jour. Suffisant pour ~50 matchs par jour!

## 📖 Utilisation

Le pipeline fonctionne en **deux phases**:

### Phase 1: Enregistrement en Direct (Pendant le Match)

Exécuter ceci **AVANT** de commencer votre match CS2:

```bash
python main.py live
```

**Ce qui se passe:**
1. ✅ Se connecte à OBS WebSocket
2. ✅ Démarre l'enregistrement automatiquement
3. ✅ Démarre le serveur GSI sur le port 3000
4. ✅ Enregistre tous les événements de jeu avec des timestamps vidéo précis

Jouez votre match normalement. Quand vous avez fini, appuyez sur `Ctrl+C` pour arrêter l'enregistrement.

Les événements sont sauvegardés dans `match_log.json`.

### Phase 2: Post-Traitement (Après le Match)

Exécuter ceci **APRÈS** le match pour créer les clips de moments forts:

```bash
python main.py process <chemin_enregistrement.mp4> [cle_api] [priorite_min]
```

**Exemple:**
```bash
python main.py process "C:\Videos\cs2_match.mp4" 6
```

**Paramètres:**
- `<chemin_enregistrement.mp4>` - Chemin vers votre enregistrement OBS (requis)
- `[cle_api]` - Clé API Google (optionnel si la variable d'environnement `GOOGLE_API_KEY` est définie)
- `[priorite_min]` - Priorité minimale du clip 1-10 (par défaut: 6)

**Ce qui se passe:**
1. 🤖 L'IA analyse `match_log.json`
2. 🎯 Identifie les moments forts (multi-kills, clutchs, headshots)
3. ✂️ Crée des clips vidéo verticaux dans le dossier `highlights/`

## 🎬 Format de Sortie

**Spécifications Vidéo Verticale:**
- **Résolution:** 1080×1920 (rapport d'aspect 9:16)
- **Format:** MP4 (H.264)
- **Audio:** AAC stéréo
- **Style Visuel:** Arrière-plan flouté + gameplay centré

**Convention de Nommage:**
```
clip_01_3k_headshot_p9.mp4
clip_02_clutch_1v3_p8.mp4
clip_03_ace_p10.mp4
```

## 🐛 Dépannage

### Problèmes de Connexion OBS
- ✅ Assurez-vous qu'OBS Studio est lancé
- ✅ Vérifiez que le WebSocket est activé: **Outils → Paramètres du Serveur WebSocket**
- ✅ Vérifiez que le port et le mot de passe correspondent à votre configuration

### Aucun Événement Enregistré
- ✅ Vérifiez que `gamestate_integration_highlights.cfg` est dans le bon dossier CS2
- ✅ Vérifiez que le serveur GSI fonctionne (devrait afficher "Listening on port 3000")
- ✅ Lancez CS2 et vérifiez la console pour les messages de connexion GSI

### Erreurs FFmpeg
- ✅ Assurez-vous que FFmpeg est installé: `ffmpeg -version`
- ✅ Vérifiez que le chemin de la vidéo source est correct
- ✅ Essayez de définir `use_gpu: False` si vous rencontrez des erreurs NVENC

### L'IA ne Retourne Aucun Moment Fort
- ✅ Vérifiez que `match_log.json` contient des événements de kill
- ✅ Baissez le seuil `min_priority` (essayez 4 ou 5)
- ✅ Vérifiez que votre clé API Google est valide: lancez `python examples/test_gemini_api.py`
- ✅ Vérifiez que vous n'avez pas dépassé le quota quotidien (1500 requêtes)

## 🤝 Contribuer

Les contributions sont les bienvenues! N'hésitez pas à soumettre une Pull Request. Pour des changements majeurs, veuillez d'abord ouvrir une issue pour discuter de ce que vous aimeriez changer.

Consultez [CONTRIBUTING.md](../../CONTRIBUTING.md) pour plus de détails.

## 📝 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](../../LICENSE) pour plus de détails.

**Résumé:** Vous pouvez librement utiliser, modifier et distribuer ce code, mais vous devez inclure l'avis de copyright original et ne pouvez pas tenir les auteurs responsables.

## 🙏 Remerciements

### Construit Avec
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - Client Python pour OBS WebSocket
- [Google Gemini API](https://ai.google.dev/) - Analyse de moments forts par IA
- [FFmpeg](https://ffmpeg.org/) - Moteur de traitement vidéo

### Assistance IA
Des parties de la base de code de ce projet ont été créées avec l'assistance de modèles de langage IA (Google Gemini, Claude) pour accélérer le développement et améliorer la qualité du code. Tout le code généré par IA a été revu, testé et adapté pour ce cas d'usage spécifique.

---

**Fait avec ❤️ par des joueurs, pour des joueurs.**

**Mettez une étoile ⭐ à ce repo si vous l'avez trouvé utile!**
