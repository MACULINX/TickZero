# TickZero Landing Page (GitHub Pages)

This branch contains the landing page for the TickZero project, hosted via GitHub Pages.

## 🌐 Live Site
Once deployed, the landing page will be available at: `https://maculinx.github.io/TickZero/`

## 📁 Structure

```
├── index.html              # Main landing page
├── assets/
│   ├── css/
│   │   └── style.css      # Stylesheet with design system
│   ├── js/
│   │   └── main.js        # Interactive features & GitHub API
│   └── images/
│       └── logo.png       # TickZero logo
├── LOGO_PROMPTS.md        # Alternative logo generation prompts
└── README.md              # This file
```

## ✨ Features

### Design
- **Professional & Modern**: Clean, minimalist design with smooth animations
- **Fully Responsive**: Mobile-first approach, works on all devices
- **Performance Optimized**: Fast loading, efficient CSS and JavaScript
- **Accessible**: Semantic HTML, ARIA labels, keyboard navigation

### Functionality
- **GitHub Integration**: Real-time download and star count via GitHub API
- **Interactive FAQ**: Accordion-style frequently asked questions
- **Smooth Scrolling**: Navigation with smooth scroll behavior
- **Copy to Clipboard**: Quick copy of installation commands
- **Scroll Animations**: Elements reveal on scroll for better UX
- **Project Roadmap**: Visual timeline of development progress

### Sections
1. **Hero**: Eye-catching introduction with CTA buttons
2. **Features**: 6 key features with icons and descriptions
3. **How It Works**: 3-step process explanation
4. **Roadmap**: Development timeline from v1.0 to v3.0
5. **FAQ**: 9 common questions with detailed answers
6. **Download**: Multiple download options with quick start guide
7. **Footer**: Links, resources, and social media

## 🚀 Local Development

To test the landing page locally:

### Option 1: Python HTTP Server
```bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000
```

### Option 2: Live Server (VS Code)
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### Option 3: Simple HTTP Server (Node.js)
```bash
npx http-server -p 8000
```

## 📝 Customization

### Update Content
Edit `index.html` to modify:
- Text content
- Links and URLs
- Section order
- Add/remove features

### Modify Styling
Edit `assets/css/style.css`:
- Colors: Modify CSS variables in `:root`
- Typography: Change font family and sizes
- Spacing: Adjust spacing scale
- Animations: Customize transitions and effects

### Update JavaScript
Edit `assets/js/main.js`:
- GitHub repo reference (line 10-11)
- Analytics integration
- Custom interactions

### Replace Logo
Replace `assets/images/logo.png` with your own logo, or use the prompts in `LOGO_PROMPTS.md` to generate alternatives.

## 🎨 Design System

The landing page uses a comprehensive design system with CSS variables:

**Colors**
- Primary: `#0066ff` (Blue)
- Secondary: `#00d4ff` (Cyan)
- Accent: `#00ff88` (Green)

**Typography**
- Font Family: Inter
- Weights: 300, 400, 500, 600, 700, 800

**Spacing Scale**
- XS: 0.5rem
- SM: 1rem
- MD: 1.5rem
- LG: 2rem
- XL: 3rem
- 2XL: 4rem
- 3XL: 6rem

## 📊 GitHub Pages Deployment

### First Time Setup
1. Ensure this branch (gh-pages) is pushed to GitHub
2. Go to repository Settings → Pages
3. Select Source: "Deploy from a branch"
4. Select Branch: "gh-pages" and folder: "/ (root)"
5. Click Save

### Updates
Simply push changes to the gh-pages branch:
```bash
git add .
git commit -m "Update landing page"
git push origin gh-pages
```

GitHub Pages will automatically rebuild and deploy within 1-2 minutes.

## 🔧 Maintenance

### Update Download/Star Counts
The JavaScript automatically fetches real-time data from GitHub API. No manual updates needed!

### Update Roadmap
Edit the timeline items in `index.html` (search for "timeline-item"):
- Change status: `completed`, `in-progress`, or `planned`
- Update version numbers and features
- Add new timeline items as needed

### Update FAQ
Add new FAQ items in `index.html` following this structure:
```html
<div class="faq-item">
    <button class="faq-question">
        <span>Your question here?</span>
        <svg class="faq-icon">...</svg>
    </button>
    <div class="faq-answer">
        <p>Your answer here.</p>
    </div>
</div>
```

## 🎯 SEO Optimization

The landing page includes:
- ✅ Semantic HTML structure
- ✅ Meta descriptions and keywords
- ✅ Open Graph tags for social sharing
- ✅ Proper heading hierarchy (H1, H2, H3)
- ✅ Alt text for images
- ✅ Fast loading performance

### Improve SEO Further
1. Add Google Analytics (add tracking ID in `main.js`)
2. Submit sitemap to Google Search Console
3. Add robots.txt if needed
4. Consider adding schema.org markup

## 📱 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Troubleshooting

**GitHub stats not loading?**
- Check browser console for API errors
- Verify repository name is correct in `main.js`
- GitHub API has rate limits (60 requests/hour unauthenticated)

**Styles not applying?**
- Clear browser cache
- Check CSS file path in `index.html`
- Verify CSS file exists at `assets/css/style.css`

**Mobile menu not working?**
- Check JavaScript console for errors
- Verify `main.js` is loaded
- Test on actual mobile device, not just responsive mode

## 📄 License

This landing page is part of the TickZero project and follows the same MIT License.

---

**Built with ❤️ for the TickZero project**
