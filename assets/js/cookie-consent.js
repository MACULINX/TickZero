// ===================================
// GDPR Cookie Consent Manager
// ===================================

class CookieConsent {
    constructor() {
        this.cookieName = 'tickzero_cookie_consent';
        this.consentGiven = this.getConsent();
        this.init();
    }

    init() {
        // Only show banner if consent hasn't been given
        if (!this.consentGiven) {
            this.showBanner();
        }

        // Setup event listeners
        this.setupEventListeners();
    }

    showBanner() {
        // Check if banner already exists
        if (document.querySelector('.cookie-consent')) {
            document.querySelector('.cookie-consent').classList.add('active');
            return;
        }

        const banner = document.createElement('div');
        banner.className = 'cookie-consent';
        banner.innerHTML = `
            <div class="cookie-consent-content">
                <div class="cookie-consent-text">
                    <h3>🍪 Cookie Notice</h3>
                    <p>
                        We use essential cookies to ensure the website functions properly. By clicking "Accept", 
                        you agree to the storing of cookies on your device. 
                        <a href="#" id="cookie-learn-more">Learn more</a> about our cookie policy.
                    </p>
                </div>
                <div class="cookie-consent-buttons">
                    <button class="cookie-btn cookie-btn-accept" id="cookie-accept">Accept</button>
                    <button class="cookie-btn cookie-btn-reject" id="cookie-reject">Reject</button>
                </div>
            </div>
        `;

        document.body.appendChild(banner);

        // Trigger animation
        setTimeout(() => {
            banner.classList.add('active');
        }, 100);
    }

    hideBanner() {
        const banner = document.querySelector('.cookie-consent');
        if (banner) {
            banner.classList.remove('active');
            setTimeout(() => {
                banner.remove();
            }, 400); // Wait for animation
        }
    }

    setupEventListeners() {
        // Accept button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'cookie-accept') {
                this.acceptCookies();
            }
        });

        // Reject button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'cookie-reject') {
                this.rejectCookies();
            }
        });

        // Learn more link
        document.addEventListener('click', (e) => {
            if (e.target.id === 'cookie-learn-more') {
                e.preventDefault();
                this.showCookiePolicy();
            }
        });
    }

    acceptCookies() {
        this.setConsent('accepted');
        this.hideBanner();
        console.log('Cookies accepted');

        // Track acceptance (only if analytics are enabled)
        if (typeof Analytics !== 'undefined') {
            Analytics.trackEvent('cookie_consent', 'accept', 'gdpr');
        }
    }

    rejectCookies() {
        this.setConsent('rejected');
        this.hideBanner();
        console.log('Cookies rejected');

        // Clear any non-essential cookies
        this.clearNonEssentialCookies();
    }

    setConsent(status) {
        const consentData = {
            status: status,
            timestamp: new Date().toISOString(),
            version: '1.0'
        };
        localStorage.setItem(this.cookieName, JSON.stringify(consentData));
        this.consentGiven = status;
    }

    getConsent() {
        const consent = localStorage.getItem(this.cookieName);
        if (!consent) return null;

        try {
            const data = JSON.parse(consent);
            return data.status;
        } catch (e) {
            return null;
        }
    }

    clearNonEssentialCookies() {
        // Clear all cookies except essential ones
        const cookies = document.cookie.split(';');

        const essentialCookies = [this.cookieName];

        cookies.forEach(cookie => {
            const cookieName = cookie.split('=')[0].trim();
            if (!essentialCookies.includes(cookieName)) {
                document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
            }
        });
    }

    showCookiePolicy() {
        // Simple modal with cookie policy
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10001;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        `;

        modal.innerHTML = `
            <div style="
                background: white;
                border-radius: 12px;
                padding: 2rem;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
            ">
                <h2 style="margin-top: 0;">Cookie Policy</h2>
                <h3>What are cookies?</h3>
                <p>Cookies are small text files stored on your device when you visit a website.</p>
                
                <h3>Essential Cookies</h3>
                <p>We use only essential cookies to:</p>
                <ul>
                    <li>Remember your language preference</li>
                    <li>Store your cookie consent choice</li>
                    <li>Ensure the website functions properly</li>
                </ul>

                <h3>Third-Party Services</h3>
                <p>We do not use analytics, advertising, or tracking cookies. This is a static landing page hosted on GitHub Pages.</p>

                <h3>Your Rights</h3>
                <p>You can change your cookie preferences at any time by clearing your browser's localStorage for this site.</p>

                <button onclick="this.closest('div').parentElement.remove()" style="
                    background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);
                    color: white;
                    border: none;
                    padding: 0.75rem 2rem;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 1rem;
                ">Close</button>
            </div>
        `;

        document.body.appendChild(modal);

        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    // Public method to check if analytics are allowed
    static canUseAnalytics() {
        const consent = localStorage.getItem('tickzero_cookie_consent');
        if (!consent) return false;

        try {
            const data = JSON.parse(consent);
            return data.status === 'accepted';
        } catch (e) {
            return false;
        }
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CookieConsent;
}
