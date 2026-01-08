#!/usr/bin/env python3
"""
Complete translation automation for remaining language pages
Uses README.xx.md files as translation source
"""

import re
from pathlib import Path

# Translation mappings from README files
FRENCH_TRANSLATIONS = {
    # How It Works section
    "How It Works": "Comment Ça Marche",
    "From gameplay to viral content in three simple steps": "Du gameplay au contenu viral en trois étapes simples",
    "Play CS2": "Jouez à CS2",
    "Launch TickZero's live logging mode before your match": "Lancez le mode d'enregistrement en direct de TickZero avant votre match",
    "The system automatically starts recording when the first round goes live": "Le système démarre automatiquement l'enregistrement lorsque le premier round commence",
    "and captures every kill, headshot, and clutch moment with precise timestamps": "et capture chaque kill, headshot et moment clutch avec des timestamps précis",
    "AI Analysis": "Analyse IA",
    "After your match, Google Gemini AI analyzes your gameplay log to identify highlight-worthy moments": "Après votre match, l'IA Google Gemini analyse le journal de votre gameplay pour identifier les moments dignes d'être mis en avant",
    "It prioritizes aces, multi-kills, clutches, headshot streaks, and high-skill plays": "Elle priorise les aces, multi-kills, clutchs, séries de headshots et actions de haute compétence",
    "Multi-kills (2K, 3K, 4K, ACE)": "Multi-kills (2K, 3K, 4K, ACE)",
    "Clutch situations (1v2, 1v3, 1v4)": "Situations clutch (1v2, 1v3, 1v4)",
    "Headshot streaks": "Séries de headshots",
    "Low health clutches": "Clutchs avec peu de vie",
    "Export & Share": "Exporter et Partager",
    "TickZero automatically generates vertical (9:16) clips optimized for TikTok and Reels": "TickZero génère automatiquement des clips verticaux (9:16) optimisés pour TikTok et Reels",
    "Each clip is hardware-accelerated, professionally formatted, and ready to upload": "Chaque clip est accéléré matériellement, formaté professionnellement et prêt à être téléchargé",
    "Resolution:": "Résolution:",
    "Duration:": "Durée:",
    "Format:": "Format:",
    
    # Roadmap section  
    "Development Roadmap": "Feuille de Route de Développement",
    "Our vision for the future of TickZero": "Notre vision pour l'avenir de TickZero",
    "v1.0 - Core Foundation": "v1.0 - Fondements de Base",
    "Completed": "Terminé",
    "Game State Integration with CS2": "Intégration d'État de Jeu avec CS2",
    "OBS WebSocket synchronization": "Synchronisation OBS WebSocket",
    "Basic AI highlight detection": "Détection de base des moments forts par IA",
    "Vertical video conversion": "Conversion vidéo verticale",
    "v1.5 - Enhanced Features": "v1.5 - Fonctionnalités Améliorées",
    "Multi-GPU hardware acceleration": "Accélération matérielle multi-GPU",
    "Continuous recording mode": "Mode d'enregistrement continu",
    "Unified launcher interface": "Interface de lancement unifiée",
    "Match history browser": "Navigateur d'historique de matchs",
    "Automatic match end detection": "Détection automatique de fin de match",
    "v2.0 - Smart Editing": "v2.0 - Édition Intelligente",
    "In Progress": "En Cours",
    "Enhanced AI clip selection": "Sélection de clips IA améliorée",
    "Custom clip templates": "Modèles de clips personnalisés",
    "Automatic captions/subtitles": "Légendes/sous-titres automatiques",
    "Music and effects library": "Bibliothèque de musique et d'effets",
    "v2.5 - Social Integration": "v2.5 - Intégration Sociale",
    "Planned": "Planifié",
    "Direct TikTok/Reels upload": "Téléchargement direct sur TikTok/Reels",
    "Auto-generated descriptions and hashtags": "Descriptions et hashtags auto-générés",
    "Thumbnail generation": "Génération de miniatures",
    "Content scheduling": "Planification de contenu",
    "v3.0 - Advanced Features": "v3.0 - Fonctionnalités Avancées",
    "Multi-game support (Valorant, Overwatch)": "Support multi-jeux (Valorant, Overwatch)",
    "Team collaboration features": "Fonctionnalités de collaboration d'équipe",
    "Advanced analytics dashboard": "Tableau de bord analytique avancé",
    "Custom AI training for personal style": "Entraînement IA personnalisé pour style personnel",
    
    # FAQ section
    "Frequently Asked Questions": "Questions Fréquemment Posées",
    "Everything you need to know about TickZero": "Tout ce que vous devez savoir sur TickZero",
    "Is TickZero really free?": "TickZero est-il vraiment gratuit?",
    "Yes! TickZero is 100% free and open-source under the MIT License": "Oui! TickZero est 100% gratuit et open-source sous licence MIT",
    "It uses Google Gemini's free tier (1500 requests/day), which is enough for approximately 50 matches per day": "Il utilise le niveau gratuit de Google Gemini (1500 requêtes/jour), ce qui est suffisant pour environ 50 matchs par jour",
    "No credit card required, no hidden costs": "Aucune carte bancaire requise, aucun coût caché",
    "What do I need to get started?": "De quoi ai-je besoin pour commencer?",
    "You'll need:": "Vous aurez besoin de:",
    "Python 3.10 or higher": "Python 3.10 ou supérieur",
    "OBS Studio with WebSocket plugin": "OBS Studio avec plugin WebSocket",
    "Counter-Strike 2": "Counter-Strike 2",
    "FFmpeg (for video processing)": "FFmpeg (pour le traitement vidéo)", 
    "A free Google API key for Gemini": "Une clé API Google gratuite pour Gemini",
    "All installation instructions are included in the documentation": "Toutes les instructions d'installation sont incluses dans la documentation",
   
    # Download section
    "Ready to Create Content?": "Prêt à Créer du Contenu?",
    "Get started with TickZero in seconds": "Commencez avec TickZero en quelques secondes",
    "No credit card required": "Aucune carte bancaire requise",
    "Download ZIP": "Télécharger ZIP",
    "Clone Repository": "Cloner le Dépôt",
    "Quick Start:": "Démarrage Rapide:",
    
    # Footer
    "Quick Links": "Liens Rapides",
    "Resources": "Ressources",
    "Documentation": "Documentation",
    "Report Issues": "Signaler des Problèmes",
    "Discussions": "Discussions",
    "Contributing": "Contribuer",
    "Legal": "Légal",
    "MIT License": "Licence MIT",
    "About Developer": "À Propos du Développeur",
    "Made with": "Fait avec",
    "by": "par",
    "Open source under MIT License": "Open source sous Licence MIT",
    "AI-powered highlight extraction for CS2 players and content creators": "Extraction de moments forts par IA pour les joueurs et créateurs de contenu CS2",
}

def translate_french_page():
    """Apply all French translations to index.fr.html"""
    filepath = Path("D:/TickZero/TickZero_ghpages/index.fr.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    for english, french in FRENCH_TRANSLATIONS.items():
        content = content.replace(english, french)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ French translation completed: {filepath}")

if __name__ == '__main__':
    translate_french_page()
