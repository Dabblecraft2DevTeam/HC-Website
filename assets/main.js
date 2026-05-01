// Security: Frame-busting script to prevent clickjacking
if (window.top !== window.self) {
    window.top.location = window.self.location;
}

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.setAttribute('aria-expanded', 'false');

        menuToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('active');
            menuToggle.classList.toggle('open', isOpen);
            menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            menuToggle.setAttribute('aria-label', isOpen ? 'Close Menu' : 'Open Menu');
        });
    }

    // Click to copy for server IP address
    const serverAddresses = document.querySelectorAll('.server-address');
    serverAddresses.forEach(address => {
        address.setAttribute('role', 'button');
        address.setAttribute('tabindex', '0');
        address.setAttribute('aria-label', 'Copy server IP address');
        address.setAttribute('title', 'Click to copy IP');

        const originalText = address.textContent;
        let timeoutId;

        const copyText = async () => {
            try {
                await navigator.clipboard.writeText(originalText);
                address.textContent = 'Copied!';
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                timeoutId = setTimeout(() => {
                    address.textContent = originalText;
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
