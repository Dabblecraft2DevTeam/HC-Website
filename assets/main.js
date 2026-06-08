if (window.self === window.top) {
    document.body.classList.remove('anti-clickjack');
} else {
    try {
        window.top.location = window.self.location;
    } catch (e) {
        // Prevent DOMException from leaking stack traces in restrictive sandboxes
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.setAttribute('aria-expanded', 'false');

        const closeMenu = () => {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('open');
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.setAttribute('aria-label', 'Open Menu');
        };

        menuToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('active');
            menuToggle.classList.toggle('open', isOpen);
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menuToggle.setAttribute('aria-label', isOpen ? 'Close Menu' : 'Open Menu');
        });

        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('active') && !menuToggle.contains(e.target) && !navLinks.contains(e.target)) {
                closeMenu();
            }
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                closeMenu();
                menuToggle.focus();
            }
        });
    }

    // Click to copy for server IP address
    const serverAddresses = document.querySelectorAll('.server-address');
    serverAddresses.forEach(address => {
        address.setAttribute('role', 'button');
        address.setAttribute('tabindex', '0');
        address.setAttribute('aria-label', 'Copy server IP address');
        address.setAttribute('title', 'Click to copy IP');
        address.setAttribute('aria-live', 'polite');

        const originalText = address.textContent;
        const originalAriaLabel = address.getAttribute('aria-label');
        const originalTitle = address.getAttribute('title');
        let timeoutId;

        const copyText = async () => {
            try {
                await navigator.clipboard.writeText(originalText);
                address.textContent = 'Copied!';
                address.setAttribute('aria-label', 'Server IP address copied!');
                address.setAttribute('title', 'Copied!');

                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                timeoutId = setTimeout(() => {
                    address.textContent = originalText;

                    if (originalAriaLabel === null) {
                        address.removeAttribute('aria-label');
                    } else {
                        address.setAttribute('aria-label', originalAriaLabel);
                    }

                    if (originalTitle === null) {
                        address.removeAttribute('title');
                    } else {
                        address.setAttribute('title', originalTitle);
                    }
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
            }
        };

        address.addEventListener('click', copyText);
        address.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                copyText();
            }
        });
    });
});
