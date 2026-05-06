if (window.self === window.top) {
    document.body.classList.remove('anti-clickjack');
} else {
    window.top.location = window.self.location;
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

        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent document click from immediately closing it
            const isOpen = navLinks.classList.toggle('active');
            menuToggle.classList.toggle('open', isOpen);
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menuToggle.setAttribute('aria-label', isOpen ? 'Close Menu' : 'Open Menu');
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                closeMenu();
                menuToggle.focus();
            }
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('active') && !navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
                closeMenu();
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
        let timeoutId;

        const copyText = async () => {
            try {
                await navigator.clipboard.writeText(originalText);
                address.textContent = 'Copied!';
                address.setAttribute('aria-label', 'Server IP address copied!');
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                timeoutId = setTimeout(() => {
                    address.textContent = originalText;
                    address.setAttribute('aria-label', 'Copy server IP address');
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
