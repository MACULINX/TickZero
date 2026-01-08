#!/usr/bin/env python3
"""
Automation script to:
1. Update canonical URLs to tickzero.maculinx.com
2. Fix French FAQ translations
3. Translate German, Russian, and Chinese pages
"""

import re
from pathlib import Path

DOMAIN = "https://tickzero.maculinx.com"

# Translation data
FAQ_TRANSLATIONS = {
    # French
    'fr': {
        "How does the AI know which moments are highlights?": "Comment l'IA identifie-t-elle les moments forts?",
        "Google Gemini analyzes your gameplay log and prioritizes moments based on:": "Google Gemini analyse le journal de votre gameplay et priorise les moments basés sur:",
        "Multi-kills:": "Multi-kills:",
        "Double kills, triples, quads, and aces": "Doubles kills, triples, quads et aces",
        "Clutch situations:": "Situations Clutch:",
        "Winning rounds when outnumbered": "Gagner des rounds en infériorité numérique",
        "Headshot accuracy:": "Précision Headshot:",
        "Precision one-tap kills": "Kills précis en un coup",
        "High-skill plays:": "Actions de haute compétence:",
        "Quick reactions and difficult shots": "Réactions rapides et tirs difficiles",
        "Clutchs avec peu de vie:": "Clutchs avec peu de vie:",
        "Surviving with minimal HP": "Survivre avec un minimum de PV",
        "You can adjust the minimum priority threshold to control how selective the AI is.": "Vous pouvez ajuster le seuil de priorité minimum pour contrôler la sélectivité de l'IA.",
        "Can I use this with other recording software besides OBS?": "Puis-je utiliser ceci avec un autre logiciel d'enregistrement qu'OBS?",
        "Currently, TickZero is designed to work with OBS Studio via WebSocket for automatic recording": "Actuellement, TickZero est conçu pour fonctionner avec OBS Studio via WebSocket pour l'enregistrement automatique",
        "control and precise timestamp synchronization. However, you can manually record with any": "contrôle et synchronisation précise des timestamps. Cependant, vous pouvez enregistrer manuellement avec n'importe quel",
        "software and process the video afterwards - you'll just need to ensure your event log": "logiciel et traiter la vidéo ensuite - vous devrez juste vous assurer que les timestamps de votre journal d'événements",
        "timestamps align with the recording start time.": "s'alignent avec l'heure de début de l'enregistrement.",
        "Will this work on Linux or Mac?": "Cela fonctionnera-t-il sur Linux ou Mac?",
        "Yes! TickZero is cross-platform and works on Windows, Linux, and macOS. The only requirement": "Oui! TickZero est multiplateforme et fonctionne sur Windows, Linux et macOS. La seule exigence",
        "is that you have Python 3.10+, OBS Studio, and FFmpeg installed on your system. CS2 Game": "est d'avoir Python 3.10+, OBS Studio et FFmpeg installés sur votre système. L'intégration d'état de jeu CS2",
        "State Integration works on all platforms as well.": "fonctionne également sur toutes les plateformes.",
        "Does it only capture my kills or teammates' kills too?": "Cela capture-t-il seulement mes kills ou aussi ceux des coéquipiers?",
        "TickZero only captures YOUR personal kills. When you die and spectate teammates, the system": "TickZero ne capture que VOS kills personnels. Lorsque vous mourez et regardez vos coéquipiers, le système",
        "automatically filters out their kills using SteamID tracking. This ensures accurate personal": "filtre automatiquement leurs kills en utilisant le suivi SteamID. Cela garantit un suivi précis des moments forts personnels",
        "highlight tracking and prevents false positives.": "et évite les faux positifs.",
        "How long does it take to process highlights?": "Combien de temps faut-il pour traiter les moments forts?",
        "Processing time depends on your hardware and the number of clips:": "Le temps de traitement dépend de votre matériel et du nombre de clips:",
        "Analyse IA:": "Analyse IA:",
        "5-10 seconds per match": "5-10 secondes par match",
        "Video Processing (GPU):": "Traitement Vidéo (GPU):",
        "2-5 seconds per clip": "2-5 secondes par clip",
        "Video Processing (CPU):": "Traitement Vidéo (CPU):",
        "10-20 seconds per clip": "10-20 secondes par clip",
        "A typical match with 3-5 highlights processes in under 1 minute with GPU acceleration.": "Un match typique avec 3-5 moments forts est traité en moins d'une minute avec accélération GPU.",
        "Can I customize the clip duration and format?": "Puis-je personnaliser la durée et le format des clips?",
        "Currently, clips are optimized for TikTok/Reels (8-15 seconds, 1080×1920). Custom durations": "Actuellement, les clips sont optimisés pour TikTok/Reels (8-15 secondes, 1080×1920). Les durées personnalisées",
        "and formats are on the roadmap for v2.0. You can modify the source code to adjust these": "et formats sont sur la feuille de route pour la v2.0. Vous pouvez modifier le code source pour ajuster ces",
        "parameters if you're comfortable with Python.": "paramètres si vous êtes à l'aise avec Python.",
        "How do I report bugs or request features?": "Comment signaler des bugs ou demander des fonctionnalités?",
        "We love community feedback! You can:": "Nous adorons les retours de la communauté! Vous pouvez:",
        "Report bugs:": "Signaler des bugs:",
        "Open an issue": "Ouvrir un ticket",
        "Request features:": "Demander des fonctionnalités:",
        "Start a discussion": "Lancer une discussion",
        "Contribute code:": "Contribuer au code:",
        "Submit a pull request": "Soumettre une pull request",
        "Get help:": "Obtenir de l'aide:",
        "Check existing issues and discussions": "Vérifier les tickets et discussions existants"
    }
}

def update_canonicals_and_domain():
    files = Path(".").glob("index*.html")
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update Canonical
        filename = filepath.name
        new_canonical = f'<link rel="canonical" href="{DOMAIN}/{filename}">'
        content = re.sub(r'<link rel="canonical" href=".*?">', new_canonical, content)
        
        # Update Hreflangs if they point to absolute URLs (checking just in case)
        # In this project they are relative, so we leave them relative.
        # But if there are any og:url, update them too.
        content = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{DOMAIN}/{filename}">', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated domain in {filename}")

def fix_french_faq():
    filepath = Path("index.fr.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for en, fr in FAQ_TRANSLATIONS['fr'].items():
        content = content.replace(en, fr)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed French FAQ")

if __name__ == "__main__":
    update_canonicals_and_domain()
    fix_french_faq()
