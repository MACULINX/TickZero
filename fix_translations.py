#!/usr/bin/env python3
"""
Final script to fix ALL remaining translation gaps in DE, RU, ZH pages.
Focuses on Hero Subtitle, Features, Footer, and Buttons.
"""

from pathlib import Path

# German Corrections
DE_FIXES = {
    # Hero Subtitle
    'Transform your CS2 gameplay into viral clips automatically using FREE AI technology.': 
    'Verwandeln Sie Ihr Counter-Strike 2 Gameplay automatisch in virale TikTok/Reels-Clips mit KOSTENLOSER KI.',
    
    'AI-powered highlight extraction for Counter-Strike 2. Automatically create TikTok and Reels-ready\n                    content from your best moments using FREE AI technology.': 
    'KI-gestützte Highlight-Extraktion für CS2. Verwandeln Sie Ihr Counter-Strike 2 Gameplay automatisch in virale TikTok/Reels-Clips mit KOSTENLOSER KI.',
    
    # Buttons
    'Download Now': 'Jetzt Herunterladen',
    'Herunterladen Now': 'Jetzt Herunterladen', # Fix previous partial replace
    
    # Stats
    'Herunterladens': 'Downloads', 
    
    # Features (Ensure full text replacement)
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS\n                        timestamp synchronization.': 
    'Erfasst Kills, Headshots und Rundenevents in Echtzeit über CS2 Game State Integration mit präziser Zeitstempel-Ausrichtung zwischen Spielereignissen und Videoaufzeichnung.',
    
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,\n                        clutches, headshots, and epic plays.':
    'Nutzt Google Gemini (KOSTENLOS) zur Identifizierung highlight-würdiger Momente: Multi-Kills, Clutches, Headshots und epische Spielzüge.',
    
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with\n                        professional quality.':
    'FFmpeg-basierte Konvertierung ins vertikale Format (9:16) mit verschwommenem Hintergrund, optimiert für TikTok und Reels.',
    
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU\n                        fallback.':
    'Automatische Hardwarebeschleunigung mit Unterstützung für NVIDIA NVENC, AMD AMF, Intel QuickSync und CPU-Fallback.',
    
    'Record multiple matches seamlessly with automatic processing between games. Perfect for marathon\n                        gaming sessions.':
    'Kontinuierliche Aufnahme: Nehmen Sie mehrere Matches nahtlos auf, mit automatischer Verarbeitung zwischen den Spielen. Perfekt für Marathon-Sessions.',
    
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -\n                        enough for ~50 matches daily).':
    'Komplett Open-Source ohne versteckte Kosten. Nutzt den KOSTENLOSEN Tarif von Google Gemini (1500 Anfragen/Tag - genug für ~50 Matches täglich).',
    
    # Footer
    'AI-powered highlight extraction for CS2 players and content creators.': 
    'KI-gesteuerte Highlight-Extraktion für CS2-Spieler und Content Creator.',
    
    'Quick Links': 'Schnelllinks',
    'Resources': 'Ressourcen',
    'Documentation': 'Dokumentation',
    'Report Issues': 'Probleme melden',
    'Discussions': 'Diskussionen',
    'Contributing': 'Mitwirken',
    'Legal': 'Rechtliches',
    'MIT License': 'MIT Lizenz',
    'About Developer': 'Über den Entwickler',
}

# Russian Corrections
RU_FIXES = {
    # Hero
    'Transform your CS2 gameplay into viral clips automatically using FREE AI technology.':
    'Автоматически превращайте свой геймплей Counter-Strike 2 в вирусные клипы для TikTok/Reels с помощью БЕСПЛАТНОГО ИИ.',
    
    'AI-powered highlight extraction for Counter-Strike 2. Automatically create TikTok and Reels-ready\n                    content from your best moments using FREE AI technology.':
    'Извлечение хайлайтов на основе ИИ для CS2. Автоматически превращайте свой геймплей Counter-Strike 2 в вирусные клипы для TikTok/Reels с помощью БЕСПЛАТНОГО ИИ.',
    
    # Buttons
    'Download Now': 'Скачать Сейчас',
    'Скачать Now': 'Скачать Сейчас', # Fix partial replace
    
    # Stats
    'Скачатьs': 'Загрузок',
    
    # Features
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS\n                        timestamp synchronization.':
    'Захватывает киллы, хедшоты и события раундов в реальном времени через CS2 Game State Integration с точной синхронизацией времени OBS.',
    
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,\n                        clutches, headshots, and epic plays.':
    'Использует Google Gemini (БЕСПЛАТНЫЙ тариф) для определения достойных моментов: мульти-киллы, клатчи, хедшоты и эпичные моменты.',
      
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with\n                        professional quality.':
    'Автоматический видеомонтаж: Конвертация на основе FFmpeg в вертикальный формат (9:16) с размытым фоном.',
    
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU\n                        fallback.':
    'Поддерживает NVIDIA NVENC, AMD AMF, Intel QuickSync с автоматическим переключением на CPU.',
    
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon\n                        игровых сессий.':
    'Записывайте несколько матчей бесшовно с автоматической обработкой между играми. Идеально для марафонских игровых сессий.',
    
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -\n                        достаточно для ~50 матчей в день).':
    'Полностью с открытым исходным кодом без скрытых затрат. Использует бесплатный уровень Google Gemini (1500 запросов/день - достаточно для ~50 матчей в день).',
    
    # Footer
    'AI-powered highlight extraction for CS2 players and content creators.':
    'Извлечение хайлайтов на основе ИИ для игроков CS2 и создателей контента.',
    
    'Quick Links': 'Быстрые ссылки',
    'Resources': 'Ресурсы',
    'Documentation': 'Документация',
    'Report Issues': 'Сообщить о проблеме',
    'Discussions': 'Обсуждения',
    'Contributing': 'Внести вклад',
    'Legal': 'Юридическая информация',
    'MIT License': 'Лицензия MIT',
    'About Developer': 'О разработчике',
}

# Chinese Corrections
ZH_FIXES = {
    # Hero
    'Transform your CS2 gameplay into viral clips automatically using FREE AI technology.':
    '使用免费AI自动将您的反恐精英2游戏画面转换为TikTok/Reels病毒短视频。',
    
    'AI-powered highlight extraction for Counter-Strike 2. Automatically create TikTok and Reels-ready\n                    content from your best moments using FREE AI technology.':
    'AI驱动的CS2高光提取工具。使用免费AI自动将您的反恐精英2游戏画面转换为TikTok/Reels病毒短视频。',
    
    # Buttons
    'Download Now': '立即下载',
    
    # Features
    'Captures kills, headshots, and round events live via CS2 Game State Integration with precise OBS\n                        timestamp synchronization.':
    '通过CS2游戏状态集成实时捕获击杀、爆头和回合事件，并与OBS时间戳精确同步。',
    
    'Google Gemini (FREE tier) intelligently identifies highlight-worthy moments: multi-kills,\n                        clutches, headshots, and epic plays.':
    '使用Google Gemini(免费套餐)智能识别值得高光的时刻：多杀、残局、爆头和精彩操作。',
    
    'FFmpeg-based conversion to vertical format (9:16) optimized for TikTok and Instagram Reels with\n                        professional quality.':
    '基于FFmpeg将视频转换为竖屏格式(9:16)并添加模糊背景，优化用于TikTok和Instagram Reels。',
    
    'Automatic hardware acceleration with support for NVIDIA NVENC, AMD AMF, Intel QuickSync, and CPU\n                        fallback.':
    '自动硬件加速，支持NVIDIA NVENC, AMD AMF, Intel QuickSync，并自动回退到CPU。',
    
    'Record multiple matches seamlessly with automatic processing between games. Pefect for marathon\n                        gaming sessions.':
    '无缝录制多场比赛，并在游戏之间自动处理。非常适合马拉松式游戏会话。',
    
    'Completely open-source with no hidden costs. Uses Google Gemini\'s FREE tier (1500 requests/day -\n                        enough for ~50 matches daily).':
    '完全开源，无隐藏费用。使用Google Gemini的免费层级（1500次请求/天 - 足够每天约50场比赛）。',
    
    # Footer
    'AI-powered highlight extraction for CS2 players and content creators.':
    '为CS2玩家和内容创作者提供的AI驱动高光提取工具。',
    
    'Quick Links': '快速链接',
    'Resources': '资源',
    'Documentation': '文档',
    'Report Issues': '报告问题',
    'Discussions': '讨论区',
    'Contributing': '贡献代码',
    'Legal': '法律信息',
    'MIT License': 'MIT 许可证',
    'About Developer': '关于开发者',
}


def fix_page(file_path, fixes):
    print(f"Fixing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        initial_len = len(content)
        
        for en, translated in fixes.items():
            # Try exact match first
            if en in content:
                content = content.replace(en, translated)
            else:
                # Try normalized whitespace match
                # This handles newlines in HTML source that might differ from strings
                import re
                escaped_en = re.escape(en).replace(r'\ ', r'\s+')
                content = re.sub(escaped_en, translated, content, flags=re.DOTALL)
                
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {file_path}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")

if __name__ == '__main__':
    fix_page('index.de.html', DE_FIXES)
    fix_page('index.ru.html', RU_FIXES)
    fix_page('index.zh.html', ZH_FIXES)
