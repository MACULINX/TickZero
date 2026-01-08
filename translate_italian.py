#!/usr/bin/env python3
"""
Script to fully translate index.it.html directly from README.it.md content
and apply standard translations for UI elements.
"""

from pathlib import Path

# UI Translations
IT_MAP = {
    # Nav & UI
    'aria-label="Select language"': 'aria-label="Seleziona lingua"',
    'Features': 'Funzionalità',
    'How It Works': 'Come Funziona',
    'Roadmap': 'Roadmap',
    'FAQ': 'Domande Frequenti',
    'Download': 'Download',
    'View on GitHub': 'Vedi su GitHub',
    
    # Hero
    'Transform Your CS2 Gameplay Into': 'Trasforma il tuo Gameplay CS2 in',
    '<span class="gradient-text">Viral Clips</span>': '<span class="gradient-text">Clip Virali</span>',
    'AI-powered highlight extraction for Counter-Strike 2.': 'Estrazione highlight guidata da IA per Counter-Strike 2.',
    'Automatically create TikTok and Reels-ready': 'Crea automaticamente contenuti pronti per TikTok e Reels',
    'content from your best moments using FREE AI technology.': 'dai tuoi momenti migliori usando tecnologia IA GRATUITA.',
    'Download Now': 'Scarica Ora',
    'Downloads': 'Download',
    'GitHub Stars': 'Stelle GitHub',
    'Free & Open': 'Gratuito e Open',
    
    # Features
    'Why Choose TickZero?': 'Perché Scegliere TickZero?',
    'Everything you need to turn your gameplay into content-ready highlights': 'Tutto ciò di cui hai bisogno per trasformare il tuo gameplay in highlight pronti da pubblicare',
    'Real-Time Event Logging': 'Logging Live degli Eventi',
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS': 'Cattura kill, headshot ed eventi round in tempo reale tramite Game State Integration di CS2 con precisa',
    'timestamp synchronization.': 'sincronizzazione dei timestamp OBS.',
    'AI-Powered Analysis': 'Analisi Potenziata da IA',
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,': 'Google Gemini (tier GRATUITO) identifica intelligentemente i momenti degni di highlight: multi-kill,',
    'clutches, headshots, and epic plays.': 'clutch, headshot e giocate epiche.',
    'Automatic Video Editing': 'Editing Video Automatico',
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with': 'Conversione basata su FFmpeg in formato verticale (9:16) ottimizzata per TikTok e Instagram Reels con',
    'professional quality.': 'qualità professionale.',
    'Multi-GPU Support': 'Supporto Multi-GPU',
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU': 'Accelerazione hardware automatica con supporto per NVIDIA NVENC, AMD AMF, Intel QuickSync e fallback',
    'fallback.': 'CPU.',
    'Continuous Recording': 'Registrazione Continua',
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon': 'Registra più partite senza interruzioni con elaborazione automatica tra i match. Perfetto per maratone',
    'gaming sessions.': 'di gioco.',
    '100% Free': '100% Gratuito',
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -': 'Completamente open-source senza costi nascosti. Usa il tier GRATUITO di Google Gemini (1500 richieste/gg -',
    'enough for ~50 matches daily).': 'abbastanza per ~50 partite al giorno).',

    # How It Works
    'From gameplay to viral content in three simple steps': 'Dal gameplay al contenuto virale in tre semplici passaggi',
    'Play CS2': 'Gioca a CS2',
    'Launch TickZero\'s live logging mode before your match.': 'Avvia la modalità di logging live di TickZero prima della partita.',
    'The system automatically starts recording when the first round goes live': 'Il sistema avvia automaticamente la registrazione quando il primo round diventa live',
    'and captures every kill, headshot, and clutch moment with precise timestamps.': 'e cattura ogni kill, headshot e momento clutch con timestamp precisi.',
    'AI Analysis': 'Analisi IA',
    'After your match, Google Gemini AI analyzes your gameplay log to identify highlight-worthy moments.': 'Dopo la partita, l\'IA di Google Gemini analizza il log di gioco per identificare i momenti migliori.',
    'It prioritizes aces, multi-kills, clutches, headshot streaks, and high-skill plays.': 'Dà priorità ad ace, multi-kill, clutch, serie di headshot e giocate ad alta abilità.',
    'Export & Share': 'Esporta e Condividi',
    'TickZero automatically generates vertical (9:16) clips optimized for TikTok and Reels.': 'TickZero genera automaticamente clip verticali (9:16) ottimizzate per TikTok e Reels.',
    'Each clip is hardware-accelerated, professionally formatted, and ready to upload.': 'Ogni clip è accelerata via hardware, formattata professionalmente e pronta per l\'upload.',
    
    # FAQ
    'Frequently Asked Questions': 'Domande Frequenti',
    'Everything you need to know about TickZero': 'Tutto ciò che devi sapere su TickZero',
    'Is TickZero really free?': 'TickZero è davvero gratuito?',
    'Yes! TickZero is 100% free and open-source under the MIT License': 'Sì! TickZero è 100% gratuito e open-source sotto Licenza MIT',
    'It uses Google Gemini\'s free tier (1500 requests/day), which is enough for approximately 50 matches per day': 'Usa il tier gratuito di Google Gemini (1500 richieste/gg), sufficiente per circa 50 partite al giorno',
    'No credit card required, no hidden costs': 'Nessuna carta di credito richiesta, nessun costo nascosto',
    'What do I need to get started?': 'Di cosa ho bisogno per iniziare?',
    'You\'ll need:': 'Avrai bisogno di:',
    'Python 3.10 or higher': 'Python 3.10 o superiore',
    'OBS Studio with WebSocket plugin': 'OBS Studio con plugin WebSocket',
    'Counter-Strike 2': 'Counter-Strike 2',
    'FFmpeg (for video processing)': 'FFmpeg (per l\'elaborazione video)',
    'A free Google API key for Gemini': 'Una chiave API Google gratuita per Gemini',
    'All installation instructions are included in the documentation': 'Tutte le istruzioni di installazione sono incluse nella documentazione',
    'How does the AI know which moments are highlights?': 'Come sa l\'IA quali sono i momenti migliori?',
    'Google Gemini analyzes your gameplay log and prioritizes moments based on:': 'Google Gemini analizza il log di gioco e prioritizza i momenti basandosi su:',
    'Multi-kills:': 'Multi-kill:',
    'Double kills, triples, quads, and aces': 'Double kill, triple, quad e ace',
    'Clutch situations:': 'Situazioni Clutch:',
    'Winning rounds when outnumbered': 'Vincere round in inferiorità numerica',
    'Headshot accuracy:': 'Precisione Headshot:',
    'Precision one-tap kills': 'Kill one-tap precise',
    'High-skill plays:': 'Giocate Alta Skill:',
    'Quick reactions and difficult shots': 'Reazioni rapide e colpi difficili',
    'Low health clutches': 'Clutch a Vita Bassa',
    'Surviving with minimal HP': 'Sopravvivere con HP minimi',
    'You can adjust the minimum priority threshold to control how selective the AI is.': 'Puoi regolare la soglia di priorità minima per controllare quanto è selettiva l\'IA.',
    'Can I use this with other recording software besides OBS?': 'Posso usarlo con altri software di registrazione oltre a OBS?',
    'Currently, TickZero is designed to work with OBS Studio via WebSocket for automatic recording': 'Attualmente, TickZero è progettato per funzionare con OBS Studio via WebSocket per la registrazione automatica',
    'control and precise timestamp synchronization. However, you can manually record with any': 'e la sincronizzazione precisa dei timestamp. Tuttavia, puoi registrare manualmente con qualsiasi',
    'software and process the video afterwards - you\'ll just need to ensure your event log': 'software e processare il video dopo - devi solo assicurarti che i timestamp del log eventi',
    'timestamps align with the recording start time.': 'siano allineati con l\'orario di inizio registrazione.',
    'Will this work on Linux or Mac?': 'Funzionerà su Linux o Mac?',
    'Yes! TickZero is cross-platform and works on Windows, Linux, and macOS. The only requirement': 'Sì! TickZero è cross-platform e funziona su Windows, Linux e macOS. L\'unico requisito',
    'is that you have Python 3.10+, OBS Studio, and FFmpeg installed on your system. CS2 Game': 'è avere Python 3.10+, OBS Studio e FFmpeg installati sul sistema. Anche la Game State',
    'State Integration works on all platforms as well.': 'Integration di CS2 funziona su tutte le piattaforme.',
    'Does it only capture my kills or teammates\' kills too?': 'Cattura solo le mie kill o anche quelle dei compagni?',
    'TickZero only captures YOUR personal kills. When you die and spectate teammates, the system': 'TickZero cattura solo le TUE kill personali. Quando muori e spetti i compagni, il sistema',
    'automatically filters out their kills using SteamID tracking. This ensures accurate personal': 'filtra automaticamente le loro kill usando il tracking SteamID. Questo garantisce un tracking accurato',
    'highlight tracking and prevents false positives.': 'degli highlight personali e previene falsi positivi.',
    'How long does it take to process highlights?': 'Quanto tempo ci vuole per processare gli highlight?',
    'Processing time depends on your hardware and the number of clips:': 'Il tempo di elaborazione dipende dal tuo hardware e dal numero di clip:',
    'Video Processing (GPU):': 'Elaborazione Video (GPU):',
    '2-5 seconds per clip': '2-5 secondi per clip',
    'Video Processing (CPU):': 'Elaborazione Video (CPU):',
    '10-20 seconds per clip': '10-20 secondi per clip',
    'A typical match with 3-5 highlights processes in under 1 minute with GPU acceleration.': 'Una partita tipica con 3-5 highlight viene processata in meno di 1 minuto con accelerazione GPU.',
    'Can I customize the clip duration and format?': 'Posso personalizzare durata e formato delle clip?',
    'Currently, clips are optimized for TikTok/Reels (8-15 seconds, 1080×1920). Custom durations': 'Attualmente, le clip sono ottimizzate per TikTok/Reels (8-15 secondi, 1080×1920). Durate',
    'and formats are on the roadmap for v2.0. You can modify the source code to adjust these': 'e formati personalizzati sono nella roadmap per la v2.0. Puoi modificare il codice sorgente per regolare',
    'parameters if you\'re comfortable with Python.': 'questi parametri se hai familiarità con Python.',
    'How do I report bugs or request features?': 'Come segnalo bug o richiedo funzionalità?',
    'We love community feedback! You can:': 'Amiamo il feedback della community! Puoi:',
    'Report bugs:': 'Segnalare bug:',
    'Open an issue': 'Apri una issue',
    'Request features:': 'Richiedere funzionalità:',
    'Start a discussion': 'Avvia una discussione',
    'Contribute code:': 'Contribuire col codice:',
    'Submit a pull request': 'Invia una pull request',
    'Get help:': 'Ottenere aiuto:',
    'Check existing issues and discussions': 'Controlla issue e discussioni esistenti',
    
    # Download
    'Ready to Create Content?': 'Pronto a Creare Contenuti?',
    'Get started with TickZero in seconds. No credit card required.': 'Inizia con TickZero in pochi secondi. Nessuna carta di credito richiesta.',
    'Quick Start:': 'Avvio Rapido:',
    'Download ZIP': 'Scarica ZIP',
    'Clone Repository': 'Clona Repository',
    'made with ❤️ by': 'fatto con ❤️ da',
    'Open source under MIT License.': 'Open source sotto Licenza MIT.',
    
    # Footer
    'Quick Links': 'Link Rapidi',
    'Resources': 'Risorse',
    'Documentation': 'Documentazione',
    'Report Issues': 'Segnala Problemi',
    'Discussions': 'Discussioni',
    'Contributing': 'Contribuire',
    'Legal': 'Legale',
    'MIT License': 'Licenza MIT',
    'About Developer': 'Info Sviluppatore',
    'AI-powered highlight extraction for CS2 players and content creators.': 'Estrazione highlight guidata da IA per giocatori e creatori di contenuti CS2.',
}

def apply_translations(file_path, translation_map):
    print(f"Translating {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for en, target in translation_map.items():
        content = content.replace(en, target)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done {file_path}")

if __name__ == '__main__':
    apply_translations('index.it.html', IT_MAP)
