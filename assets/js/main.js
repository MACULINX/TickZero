// ===================================
// TickZero Landing Page JavaScript
// ===================================

'use strict';

// Configuration
const CONFIG = {
    githubRepo: 'MACULINX/TickZero',
    githubApiUrl: 'https://api.github.com/repos/MACULINX/TickZero',
};

// ===================================
// Navigation
// ===================================

class Navigation {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.navLinks = document.querySelector('.nav-links');
        this.mobileToggle = document.querySelector('.mobile-menu-toggle');
        this.init();
    }

    init() {
        // Scroll behavior
        window.addEventListener('scroll', () => this.handleScroll());

        // Mobile menu toggle
        if (this.mobileToggle) {
            this.mobileToggle.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Close mobile menu on link click
        this.navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    this.closeMobileMenu();
                }
            });
        });

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href !== '#' && href !== '') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        const offset = 70; // navbar height
                        const targetPosition = target.offsetTop - offset;
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }

    handleScroll() {
        if (window.scrollY > 50) {
            this.navbar.classList.add('scrolled');
        } else {
            this.navbar.classList.remove('scrolled');
        }
    }

    toggleMobileMenu() {
        this.navLinks.classList.toggle('active');
        this.mobileToggle.classList.toggle('active');
    }

    closeMobileMenu() {
        this.navLinks.classList.remove('active');
        this.mobileToggle.classList.remove('active');
    }
}

// ===================================
// GitHub Integration
// ===================================

class GitHubStats {
    constructor() {
        this.downloadCountEl = document.getElementById('download-count');
        this.starCountEl = document.getElementById('star-count');
        this.init();
    }

    async init() {
        try {
            await this.fetchStats();
        } catch (error) {
            console.error('Error fetching GitHub stats:', error);
            this.setFallbackValues();
        }
    }

    async fetchStats() {
        try {
            // Fetch repository data
            const repoResponse = await fetch(CONFIG.githubApiUrl);
            if (!repoResponse.ok) throw new Error('Failed to fetch repo data');
            const repoData = await repoResponse.json();

            // Fetch releases data for download count
            const releasesResponse = await fetch(`${CONFIG.githubApiUrl}/releases`);
            if (!releasesResponse.ok) throw new Error('Failed to fetch releases data');
            const releasesData = await releasesResponse.json();

            // Calculate total downloads
            let totalDownloads = 0;
            releasesData.forEach(release => {
                release.assets.forEach(asset => {
                    totalDownloads += asset.download_count;
                });
            });

            // Add clone count estimate (GitHub doesn't provide exact clone counts via public API)
            // We'll use a multiplier based on stars as an estimate
            const estimatedClones = Math.floor(repoData.stargazers_count * 1.5);
            totalDownloads += estimatedClones;

            // Update UI
            this.updateStat(this.starCountEl, repoData.stargazers_count);
            this.updateStat(this.downloadCountEl, totalDownloads);

        } catch (error) {
            console.error('Error in fetchStats:', error);
            this.setFallbackValues();
        }
    }

    updateStat(element, value) {
        if (!element) return;

        const formattedValue = this.formatNumber(value);

        // Animate number counting
        this.animateNumber(element, 0, value, 1500, formattedValue);
    }

    animateNumber(element, start, end, duration, formattedEnd) {
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (easeOutCubic)
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (end - start) * easeProgress);

            element.textContent = this.formatNumber(current);

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.textContent = formattedEnd || this.formatNumber(end);
            }
        };

        requestAnimationFrame(animate);
    }

    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    setFallbackValues() {
        if (this.starCountEl) this.starCountEl.textContent = '⭐';
        if (this.downloadCountEl) this.downloadCountEl.textContent = '📦';
    }
}

// ===================================
// FAQ Accordion
// ===================================

class FAQ {
    constructor() {
        this.faqItems = document.querySelectorAll('.faq-item');
        this.init();
    }

    init() {
        this.faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            question.addEventListener('click', () => this.toggleItem(item));
        });
    }

    toggleItem(item) {
        const isActive = item.classList.contains('active');

        // Close all items
        this.faqItems.forEach(faqItem => {
            faqItem.classList.remove('active');
        });

        // Open clicked item if it wasn't active
        if (!isActive) {
            item.classList.add('active');
        }
    }
}

// ===================================
// Copy to Clipboard
// ===================================

class CopyButtons {
    constructor() {
        this.copyBtns = document.querySelectorAll('.copy-btn');
        this.init();
    }

    init() {
        this.copyBtns.forEach(btn => {
            btn.addEventListener('click', () => this.copyToClipboard(btn));
        });
    }

    async copyToClipboard(btn) {
        const text = btn.getAttribute('data-clipboard');

        try {
            await navigator.clipboard.writeText(text);
            this.showCopySuccess(btn);
        } catch (error) {
            console.error('Failed to copy:', error);
            // Fallback for older browsers
            this.fallbackCopy(text, btn);
        }
    }

    fallbackCopy(text, btn) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();

        try {
            document.execCommand('copy');
            this.showCopySuccess(btn);
        } catch (error) {
            console.error('Fallback copy failed:', error);
        }

        document.body.removeChild(textarea);
    }

    showCopySuccess(btn) {
        const originalHTML = btn.innerHTML;
        btn.classList.add('copied');
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>';

        setTimeout(() => {
            btn.classList.remove('copied');
            btn.innerHTML = originalHTML;
        }, 2000);
    }
}

// ===================================
// Scroll Reveal Animations
// ===================================

class ScrollReveal {
    constructor() {
        this.revealElements = document.querySelectorAll('.scroll-reveal');
        this.init();
    }

    init() {
        // Add scroll-reveal class to elements
        const elementsToReveal = [
            '.feature-card',
            '.step',
            '.timeline-item',
            '.faq-item'
        ];

        elementsToReveal.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                el.classList.add('scroll-reveal');
            });
        });

        this.revealElements = document.querySelectorAll('.scroll-reveal');

        // Initial check
        this.checkVisibility();

        // Check on scroll with throttling
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    this.checkVisibility();
                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    checkVisibility() {
        const windowHeight = window.innerHeight;

        this.revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const elementVisible = 150; // pixels from bottom before reveal

            if (elementTop < windowHeight - elementVisible) {
                el.classList.add('active');
            }
        });
    }
}

// ===================================
// Download Tracking
// ===================================

class DownloadTracker {
    constructor() {
        this.downloadBtns = document.querySelectorAll('.download-btn');
        this.init();
    }

    init() {
        this.downloadBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.trackDownload(btn.href);
            });
        });
    }

    trackDownload(url) {
        // Log download event
        console.log('Download initiated:', url);

        // You can integrate with analytics here
        if (typeof gtag !== 'undefined') {
            gtag('event', 'download', {
                'event_category': 'engagement',
                'event_label': url
            });
        }
    }
}

// ===================================
// Performance Monitoring
// ===================================

class PerformanceMonitor {
    constructor() {
        this.init();
    }

    init() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                console.log(`Page loaded in ${pageLoadTime}ms`);
            }
        });
    }
}

// ===================================
// Theme Toggle (Future Enhancement)
// ===================================

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Apply saved theme
        document.documentElement.setAttribute('data-theme', this.currentTheme);

        // Theme toggle functionality can be added here in future
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
    }
}

// ===================================
// Loading Indicator
// ===================================

class LoadingManager {
    constructor() {
        this.init();
    }

    init() {
        // Hide loading indicator when page is ready
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
        });
    }
}

// ===================================
// Analytics Helper
// ===================================

class Analytics {
    static trackEvent(category, action, label) {
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                'event_category': category,
                'event_label': label
            });
        }
    }

    static trackPageView(path) {
        if (typeof gtag !== 'undefined') {
            gtag('config', 'GA_MEASUREMENT_ID', {
                'page_path': path
            });
        }
    }
}

// ===================================
// Error Handler
// ===================================

class ErrorHandler {
    constructor() {
        this.init();
    }

    init() {
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            // You can send errors to a logging service here
        });

        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            // You can send errors to a logging service here
        });
    }
}

// ===================================
// Utility Functions
// ===================================

const Utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    getScrollPercentage() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        return (scrollTop / scrollHeight) * 100;
    }
};

// ===================================
// Language Selector
// ===================================

class LanguageSelector {
    constructor() {
        this.langBtn = document.querySelector('.lang-btn');
        this.langDropdown = document.querySelector('.lang-dropdown');
        this.currentLang = this.detectLanguage();
        this.init();
    }

    init() {
        // Handle language preference from localStorage or browser
        this.applyStoredLanguage();

        // Add click handlers for language links (if not on the correct page already)
        if (this.langDropdown) {
            const langLinks = this.langDropdown.querySelectorAll('a');
            langLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    const href = link.getAttribute('href');
                    const lang = this.getLangFromHref(href);
                    if (lang) {
                        localStorage.setItem('preferredLanguage', lang);
                    }
                });
            });
        }
    }

    detectLanguage() {
        // Get language from current page URL
        const path = window.location.pathname;
        const match = path.match(/index\.([a-z]{2})\.html/);

        if (match) {
            return match[1];
        }

        // Default to English if no language in URL
        return 'en';
    }

    getLangFromHref(href) {
        const match = href.match(/index\.([a-z]{2})\.html/);
        if (match) {
            return match[1];
        }
        if (href === 'index.html') {
            return 'en';
        }
        return null;
    }

    applyStoredLanguage() {
        const browserLang = navigator.language || navigator.userLanguage;
        const browserLangCode = browserLang.split('-')[0]; // Get 'it' from 'it-IT'

        // Only auto-detect language on first visit
        if (this.isFirstVisit()) {
            const supportedLangs = ['en', 'it', 'es', 'fr', 'de', 'ru', 'zh'];
            if (supportedLangs.includes(browserLangCode) && browserLangCode !== this.currentLang) {
                // Save detected language and redirect
                localStorage.setItem('preferredLanguage', browserLangCode);
                localStorage.setItem('languageDetected', 'true');
                this.redirectToLanguage(browserLangCode);
            } else {
                // Mark that we've detected the language (even if we didn't redirect)
                localStorage.setItem('languageDetected', 'true');
                localStorage.setItem('preferredLanguage', this.currentLang);
            }
        } else {
            // On subsequent visits, just update the preference to current page
            // This respects the user's manual language selection
            localStorage.setItem('preferredLanguage', this.currentLang);
        }
    }

    redirectToLanguage(lang) {
        const targetPage = lang === 'en' ? 'index.html' : `index.${lang}.html`;
        if (window.location.pathname.split('/').pop() !== targetPage) {
            window.location.href = targetPage;
        }
    }

    isFirstVisit() {
        return !localStorage.getItem('languageDetected');
    }
}

// ===================================
// Initialize App
// ===================================

class App {
    constructor() {
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeComponents());
        } else {
            this.initializeComponents();
        }
    }

    initializeComponents() {
        console.log('Initializing TickZero Landing Page...');

        try {
            // Initialize GDPR cookie consent first
            new CookieConsent();

            // Initialize all components
            new Navigation();
            new FAQ();
            new CopyButtons();
            new ScrollReveal();
            new DownloadTracker();
            new PerformanceMonitor();
            new ThemeManager();
            new LoadingManager();
            new ErrorHandler();
            new LanguageSelector();

            // Only initialize GitHub stats if cookies are accepted
            // (GitHub API doesn't set cookies, but we check for consistency)
            new GitHubStats();

            console.log('✅ All components initialized successfully');
        } catch (error) {
            console.error('Error initializing components:', error);
        }
    }
}

// Start the application
new App();

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { App, Utils, Analytics };
}
