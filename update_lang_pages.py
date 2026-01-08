#!/usr/bin/env python3
"""
Script to batch update all language pages with SVG flags and GDPR compliance
"""

import re
from pathlib import Path

# Language page files to update (excluding English and Italian which are already done)
LANG_FILES = {
    'index.es.html': 'es',
    'index.fr.html': 'fr',
    'index.de.html': 'de',
    'index.ru.html': 'ru',
    'index.zh.html': 'zh'
}

FLAG_CLASSES = {
    'en': 'flag-gb',
    'it': 'flag-it',
    'es': 'flag-es',
    'fr': 'flag-fr',
    'de': 'flag-de',
    'ru': 'flag-ru',
    'zh': 'flag-zh'
}

def update_language_page(filepath, lang_code):
    """Update a single language page with SVG flags and GDPR"""
    print(f"Updating {filepath} ({lang_code})...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add flags.css and cookie-consent.css after style.css
    if 'flags.css' not in content:
        content = content.replace(
            '<link rel="stylesheet" href="assets/css/style.css">',
            '''<link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/flags.css">
    <link rel="stylesheet" href="assets/css/cookie-consent.css">'''
        )
    
    # 2. Add canonical URL before </head>
    expected_canonical = f'<link rel="canonical" href="https://maculinx.github.io/TickZero/index.{lang_code}.html">'
    if expected_canonical not in content:
        content = content.replace('</head>', f'''    
    <!-- Canonical URL -->
    {expected_canonical}
</head>''')
    
    # 3. Replace emoji in language selector button
    button_pattern = r'<span class="flag">🇬🇧</span>|<span class="flag">🇮🇹</span>|<span class="flag">🇪🇸</span>|<span class="flag">🇫🇷</span>|<span class="flag">🇩🇪</span>|<span class="flag">🇷🇺</span>|<span class="flag">🇨🇳</span>'
    content = re.sub(button_pattern, f'<span class="flag-icon {FLAG_CLASSES[lang_code]}"></span>', content)
    
    # 4. Replace emojis in dropdown
    dropdown_replacements = [
        ('🇬🇧 English', '<span class="flag-icon flag-gb"></span>English'),
        ('🇮🇹 Italiano', '<span class="flag-icon flag-it"></span>Italiano'),
        ('🇪🇸 Español', '<span class="flag-icon flag-es"></span>Español'),
        ('🇫🇷 Français', '<span class="flag-icon flag-fr"></span>Français'),
        ('🇩🇪 Deutsch', '<span class="flag-icon flag-de"></span>Deutsch'),
        ('🇷🇺 Русский', '<span class="flag-icon flag-ru"></span>Русский'),
        ('🇨🇳 中文', '<span class="flag-icon flag-zh"></span>中文'),
    ]
    
    for emoji_text, svg_text in dropdown_replacements:
        content = content.replace(emoji_text, svg_text)
    
    # 5. Add cookie-consent.js before main.js
    if 'cookie-consent.js' not in content:
        content = content.replace(
            '<script src="assets/js/main.js"></script>',
            '''<script src="assets/js/cookie-consent.js"></script>
    <script src="assets/js/main.js"></script>'''
        )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {filepath}")

def main():
    base_dir = Path(__file__).parent
    
    for filename, lang_code in LANG_FILES.items():
        filepath = base_dir / filename
        if filepath.exists():
            update_language_page(filepath, lang_code)
        else:
            print(f"⚠️  File not found: {filepath}")
    
    print("\n✅ All language pages updated!")

if __name__ == '__main__':
    main()
