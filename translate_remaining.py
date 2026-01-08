#!/usr/bin/env python3
"""
Script to apply translations for German, Russian, and Chinese pages.
Based on README content and standard translations.
"""

from pathlib import Path

# German Translations (DE)
DE_MAP = {
    # Nav & UI
    'aria-label="Select language"': 'aria-label="Sprache wählen"',
    'Features': 'Funktionen',
    'How It Works': 'Wie es funktioniert',
    'Roadmap': 'Roadmap',
    'FAQ': 'FAQ',
    'Download': 'Herunterladen',
    'View on GitHub': 'Auf GitHub ansehen',
    
    # Hero
    'Transform Your CS2 Gameplay Into': 'Verwandeln Sie Ihr CS2-Gameplay in',
    '<span class="gradient-text">Viral Clips</span>': '<span class="gradient-text">Virale Clips</span>',
    'AI-powered highlight extraction for Counter-Strike 2.': 'KI-gestützte Highlight-Extraktion für Counter-Strike 2.',
    'Automatically create TikTok and Reels-ready': 'Erstellen Sie automatisch TikTok- und Reels-bereite',
    'content from your best moments using FREE AI technology.': 'Inhalte aus Ihren besten Momenten mit KOSTENLOSER KI-Technologie.',
    'Download Now': 'Jetzt Herunterladen',
    'Downloads': 'Downloads',
    'GitHub Stars': 'GitHub Sterne',
    'Free & Open': 'Kostenlos & Offen',
    
    # Features
    'Why Choose TickZero?': 'Warum TickZero?',
    'Everything you need to turn your gameplay into content-ready highlights': 'Alles, was Sie brauchen, um Ihr Gameplay in Content-bereite Highlights zu verwandeln',
    'Real-Time Event Logging': 'Live-Event-Logging',
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS': 'Erfasst Kills, Headshots und Rundenevents in Echtzeit über CS2 Game State Integration mit präziser OBS',
    'timestamp synchronization.': 'Zeitstempel-Synchronisation.',
    'AI-Powered Analysis': 'KI-gestützte Analyse',
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,': 'Google Gemini (KOSTENLOS) identifiziert intelligent highlight-würdige Momente: Multi-Kills,',
    'clutches, headshots, and epic plays.': 'Clutches, Headshots und epische Spielzüge.',
    'Automatic Video Editing': 'Automatische Videobearbeitung',
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with': 'FFmpeg-basierte Konvertierung in das vertikale Format (9:16), optimiert für TikTok und Instagram Reels mit',
    'professional quality.': 'professioneller Qualität.',
    'Multi-GPU Support': 'Multi-GPU Unterstützung',
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU': 'Automatische Hardwarebeschleunigung mit Unterstützung für NVIDIA NVENC, AMD AMF, Intel QuickSync und CPU',
    'fallback.': 'Fallback.',
    'Continuous Recording': 'Kontinuierliche Aufnahme',
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon': 'Nehmen Sie mehrere Matches nahtlos auf, mit automatischer Verarbeitung zwischen den Spielen. Perfekt für Marathon-',
    'gaming sessions.': 'Gaming-Sessions.',
    '100% Free': '100% Kostenlos',
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -': 'Komplett Open-Source ohne versteckte Kosten. Nutzt den KOSTENLOSEN Tarif von Google Gemini (1500 Anfragen/Tag -',
    'enough for ~50 matches daily).': 'genug für ~50 Matches täglich).',

    # How It Works
    'From gameplay to viral content in three simple steps': 'Vom Gameplay zum viralen Content in drei einfachen Schritten',
    'Play CS2': 'CS2 Spielen',
    'Launch TickZero\'s live logging mode before your match.': 'Starten Sie den Live-Logging-Modus von TickZero vor Ihrem Match.',
    'The system automatically starts recording when the first round goes live': 'Das System startet automatisch die Aufnahme, wenn die erste Runde live geht',
    'and captures every kill, headshot, and clutch moment with precise timestamps.': 'und erfasst jeden Kill, Headshot und Clutch-Moment mit präzisen Zeitstempeln.',
    'AI Analysis': 'KI-Analyse',
    'After your match, Google Gemini AI analyzes your gameplay log to identify highlight-worthy moments.': 'Nach Ihrem Match analysiert die Google Gemini KI Ihr Gameplay-Log, um highlight-würdige Momente zu identifizieren.',
    'It prioritizes aces, multi-kills, clutches, headshot streaks, and high-skill plays.': 'Es priorisiert Asse, Multi-Kills, Clutches, Headshot-Serien und High-Skill-Plays.',
    'Export & Share': 'Exportieren & Teilen',
    'TickZero automatically generates vertical (9:16) clips optimized for TikTok and Reels.': 'TickZero generiert automatisch vertikale (9:16) Clips, optimiert für TikTok und Reels.',
    'Each clip is hardware-accelerated, professionally formatted, and ready to upload.': 'Jeder Clip ist hardwarebeschleunigt, professionell formatiert und bereit zum Hochladen.',
    
    # FAQ (Simple headers)
    'Frequently Asked Questions': 'Häufig gestellte Fragen',
    'Everything you need to know about TickZero': 'Alles, was Sie über TickZero wissen müssen',
    'Is TickZero really free?': 'Ist TickZero wirklich kostenlos?',
    'What do I need to get started?': 'Was brauche ich, um anzufangen?',
    'How does the AI know which moments are highlights?': 'Woher weiß die KI, welche Momente Highlights sind?',
    'Can I use this with other recording software besides OBS?': 'Kann ich dies mit anderer Aufnahmesoftware außer OBS verwenden?',
    'Will this work on Linux or Mac?': 'Funktioniert das unter Linux oder Mac?',
    'Does it only capture my kills or teammates\' kills too?': 'Erfasst es nur meine Kills oder auch die der Teamkollegen?',
    'How long does it take to process highlights?': 'Wie lange dauert die Verarbeitung der Highlights?',
    'Can I customize the clip duration and format?': 'Kann ich die Clip-Dauer und das Format anpassen?',
    'How do I report bugs or request features?': 'Wie melde ich Fehler oder fordere Funktionen an?',
    
    # Download & Footer
    'Ready to Create Content?': 'Bereit, Inhalte zu erstellen?',
    'Get started with TickZero in seconds. No credit card required.': 'Starten Sie mit TickZero in Sekunden. Keine Kreditkarte erforderlich.',
    'Quick Start:': 'Schnellstart:',
    'Download ZIP': 'ZIP Herunterladen',
    'Clone Repository': 'Repository Klonen',
    'made with ❤️ by': 'gemacht mit ❤️ von',
}

# Russian Translations (RU)
RU_MAP = {
    # Nav & UI
    'aria-label="Select language"': 'aria-label="Выберите язык"',
    'Features': 'Возможности',
    'How It Works': 'Как это работает',
    'Roadmap': 'План развития',
    'FAQ': 'FAQ',
    'Download': 'Скачать',
    'View on GitHub': 'Смотреть на GitHub',
    
    # Hero
    'Transform Your CS2 Gameplay Into': 'Превратите ваш геймплей CS2 в',
    '<span class="gradient-text">Viral Clips</span>': '<span class="gradient-text">Вирусные Клипы</span>',
    'AI-powered highlight extraction for Counter-Strike 2.': 'Извлечение хайлайтов на базе ИИ для Counter-Strike 2.',
    'Automatically create TikTok and Reels-ready': 'Автоматически создавайте готовые для TikTok и Reels',
    'content from your best moments using FREE AI technology.': 'видео из ваших лучших моментов с помощью БЕСПЛАТНОГО ИИ.',
    'Download Now': 'Скачать Сейчас',
    'Downloads': 'Загрузок',
    'GitHub Stars': 'Звезд GitHub',
    'Free & Open': 'Бесплатно и Открыто',
    
    # Features
    'Why Choose TickZero?': 'Почему TickZero?',
    'Everything you need to turn your gameplay into content-ready highlights': 'Всё необходимое для превращения вашего геймплея в готовый контент',
    'Real-Time Event Logging': 'Запись событий в реальном времени',
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS': 'Захватывает киллы, хедшоты и события раунда в прямом эфире через CS2 Game State Integration с точной',
    'timestamp synchronization.': 'синхронизацией времени OBS.',
    'AI-Powered Analysis': 'Анализ на базе ИИ',
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,': 'Google Gemini (бесплатно) интеллектуально определяет лучшие моменты: мульти-киллы,',
    'clutches, headshots, and epic plays.': 'клатчи, хедшоты и эпичные моменты.',
    'Automatic Video Editing': 'Автоматический видеомонтаж',
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with': 'Конвертация на основе FFmpeg в вертикальный формат (9:16), оптимизированная для TikTok и Reels с',
    'professional quality.': 'профессиональным качеством.',
    'Multi-GPU Support': 'Поддержка Multi-GPU',
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU': 'Автоматическое аппаратное ускорение с поддержкой NVIDIA NVENC, AMD AMF, Intel QuickSync и CPU',
    'fallback.': 'fallback.',
    'Continuous Recording': 'Непрерывная запись',
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon': 'Записывайте несколько матчей бесшовно с автоматической обработкой между играми. Идеально для марафонских',
    'gaming sessions.': 'игровых сессий.',
    '100% Free': '100% Бесплатно',
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -': 'Полностью с открытым исходным кодом без скрытых затрат. Использует бесплатный уровень Google Gemini (1500 запросов/день -',
    'enough for ~50 matches daily).': 'достаточно для ~50 матчей в день).',

    # How It Works
    'From gameplay to viral content in three simple steps': 'От геймплея к вирусному контенту за три простых шага',
    'Play CS2': 'Играйте в CS2',
    'Launch TickZero\'s live logging mode before your match.': 'Запустите режим живого логгирования TickZero перед матчем.',
    'The system automatically starts recording when the first round goes live': 'Система автоматически начинает запись, когда начинается первый раунд',
    'and captures every kill, headshot, and clutch moment with precise timestamps.': 'и захватывает каждый килл, хедшот и клатч с точными временными метками.',
    'AI Analysis': 'Анализ ИИ',
    'After your match, Google Gemini AI analyzes your gameplay log to identify highlight-worthy moments.': 'После матча ИИ Google Gemini анализирует лог игры для выявления лучших моментов.',
    'It prioritizes aces, multi-kills, clutches, headshot streaks, and high-skill plays.': 'Приоритет отдается эйсам, мульти-киллам, клатчам, сериям хедшотов и скилловым моментам.',
    'Export & Share': 'Экспорт и Поделиться',
    'TickZero automatically generates vertical (9:16) clips optimized for TikTok and Reels.': 'TickZero автоматически создает вертикальные (9:16) клипы, оптимизированные для TikTok и Reels.',
    'Each clip is hardware-accelerated, professionally formatted, and ready to upload.': 'Каждый клип аппаратно ускорен, профессионально отформатирован и готов к загрузке.',
    
    # FAQ headers
    'Frequently Asked Questions': 'Часто задаваемые вопросы',
    'Everything you need to know about TickZero': 'Всё, что нужно знать о TickZero',
    'Is TickZero really free?': 'TickZero действительно бесплатен?',
    'What do I need to get started?': 'Что нужно для начала?',
    'How does the AI know which moments are highlights?': 'Как ИИ определяет хайлайты?',
    'Can I use this with other recording software besides OBS?': 'Можно ли использовать с другим ПО для записи кроме OBS?',
    'Will this work on Linux or Mac?': 'Будет ли это работать на Linux или Mac?',
    'Does it only capture my kills or teammates\' kills too?': 'Захватывает только мои киллы или тиммейтов тоже?',
    'How long does it take to process highlights?': 'Сколько времени занимает обработка?',
    'Can I customize the clip duration and format?': 'Можно ли настроить длительность и формат клипа?',
    'How do I report bugs or request features?': 'Как сообщить об ошибках или запросить функции?',

    # Download
    'Ready to Create Content?': 'Готовы создавать контент?',
    'Get started with TickZero in seconds. No credit card required.': 'Начните с TickZero за секунды. Кредитная карта не требуется.',
    'Quick Start:': 'Быстрый старт:',
    'Download ZIP': 'Скачать ZIP',
    'Clone Repository': 'Клонировать репозиторий',
    'made with ❤️ by': 'сделано с ❤️',
}

# Chinese Translations (ZH)
ZH_MAP = {
    # Nav & UI
    'aria-label="Select language"': 'aria-label="选择语言"',
    'Features': '功能特性',
    'How It Works': '工作原理',
    'Roadmap': '路线图',
    'FAQ': '常见问题',
    'Download': '下载',
    'View on GitHub': '在 GitHub 上查看',
    
    # Hero
    'Transform Your CS2 Gameplay Into': '将您的 CS2 游戏体验转化为',
    '<span class="gradient-text">Viral Clips</span>': '<span class="gradient-text">病毒式短视频</span>',
    'AI-powered highlight extraction for Counter-Strike 2.': '由 AI 驱动的反恐精英 2 高光时刻提取工具。',
    'Automatically create TikTok and Reels-ready': '自动创建适用于 TikTok 和 Reels 的',
    'content from your best moments using FREE AI technology.': '内容，使用免费 AI 技术捕捉您的最佳时刻。',
    'Download Now': '立即下载',
    'Downloads': '下载量',
    'GitHub Stars': 'GitHub 星数',
    'Free & Open': '免费开源',
    
    # Features
    'Why Choose TickZero?': '为什么选择 TickZero？',
    'Everything you need to turn your gameplay into content-ready highlights': '将游戏过程转化为高质量集锦所需的一切',
    'Real-Time Event Logging': '实时事件记录',
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS': '通过 CS2 游戏状态集成实时记录击杀、爆头和回合事件，并与 OBS',
    'timestamp synchronization.': '时间戳精确同步。',
    'AI-Powered Analysis': 'AI 驱动分析',
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,': 'Google Gemini（免费版）智能识别值得记录的高光时刻：多杀、',
    'clutches, headshots, and epic plays.': '残局、爆头和精彩操作。',
    'Automatic Video Editing': '自动视频剪辑',
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with': '基于 FFmpeg 转换为针对 TikTok 和 Instagram Reels 优化的竖屏格式 (9:16)，',
    'professional quality.': '具有专业品质。',
    'Multi-GPU Support': '多 GPU 支持',
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU': '自动硬件加速，支持 NVIDIA NVENC、AMD AMF、Intel QuickSync 和 CPU',
    'fallback.': '回退。',
    'Continuous Recording': '连续录制',
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon': '无缝录制多场比赛，并在游戏之间自动处理。非常适合马拉松式',
    'gaming sessions.': '游戏会话。',
    '100% Free': '100% 免费',
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -': '完全开源，无隐藏费用。使用 Google Gemini 的免费层级（1500 次请求/天 -',
    'enough for ~50 matches daily).': '足够每天约 50 场比赛）。',

    # How It Works
    'From gameplay to viral content in three simple steps': '只需三步，从游戏到病毒式内容',
    'Play CS2': '玩 CS2',
    'Launch TickZero\'s live logging mode before your match.': '在比赛前启动 TickZero 的实时记录模式。',
    'The system automatically starts recording when the first round goes live': '系统会在第一回合开始时自动开始录制',
    'and captures every kill, headshot, and clutch moment with precise timestamps.': '并捕捉每个击杀、爆头和残局时刻以及精确的时间戳。',
    'AI Analysis': 'AI 分析',
    'After your match, Google Gemini AI analyzes your gameplay log to identify highlight-worthy moments.': '比赛结束后，Google Gemini AI 会分析您的游戏日志以识别高光时刻。',
    'It prioritizes aces, multi-kills, clutches, headshot streaks, and high-skill plays.': '它会优先考虑五杀、多杀、残局、连杀爆头和高技术操作。',
    'Export & Share': '导出与分享',
    'TickZero automatically generates vertical (9:16) clips optimized for TikTok and Reels.': 'TickZero 自动生成针对 TikTok 和 Reels 优化的竖屏 (9:16) 片段。',
    'Each clip is hardware-accelerated, professionally formatted, and ready to upload.': '每个片段都经过硬件加速、专业格式化，并准备好上传。',
    
    # FAQ
    'Frequently Asked Questions': '常见问题',
    'Everything you need to know about TickZero': '关于 TickZero 你需要知道的一切',
    'Is TickZero really free?': 'TickZero 真的免费吗？',
    'What do I need to get started?': '我需要什么才能开始？',
    'How does the AI know which moments are highlights?': 'AI 如何知道哪些时刻是高光？',
    'Can I use this with other recording software besides OBS?': '除了 OBS，我可以与其他录制软件一起使用吗？',
    'Will this work on Linux or Mac?': '这可以在 Linux 或 Mac 上运行吗？',
    'Does it only capture my kills or teammates\' kills too?': '它只捕捉我的击杀还是也捕捉队友的？',
    'How long does it take to process highlights?': '处理高光时刻需要多长时间？',
    'Can I customize the clip duration and format?': '我可以自定义片段持续时间和格式吗？',
    'How do I report bugs or request features?': '如何报告错误或请求功能？',
    
    # Download
    'Ready to Create Content?': '准备好创作内容了吗？',
    'Get started with TickZero in seconds. No credit card required.': '几秒钟内开始使用 TickZero。无需信用卡。',
    'Quick Start:': '快速开始：',
    'Download ZIP': '下载 ZIP',
    'Clone Repository': '克隆仓库',
    'made with ❤️ by': '由 ❤️ 制作',
}

def apply_translations(file_path, translation_map):
    print(f"Translating {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for en, target in translation_map.items():
        # Simple replace - care taken to pick unique strings
        content = content.replace(en, target)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done {file_path}")

if __name__ == '__main__':
    apply_translations('index.de.html', DE_MAP)
    apply_translations('index.ru.html', RU_MAP)
    apply_translations('index.zh.html', ZH_MAP)
