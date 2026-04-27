## 2024-04-25 - Insecure External Links
**Vulnerability:** External links using `http://` instead of `https://` (specifically on Instagram and TikTok links), exposing users to potential MITM attacks when leaving the site. Furthermore, all external links lacked `target="_blank" rel="noopener noreferrer"`. Missing `rel="noopener noreferrer"` can expose the site to reverse tabnabbing attacks where the newly opened page can maliciously manipulate the originating page via `window.opener`.
**Learning:** Hardcoded links in static HTML files often miss the `rel="noopener noreferrer"` attribute when `target="_blank"` is not explicitly used, but even without it, external links can be used as vectors. Ensuring both HTTPS and secure target attributes is a simple but critical layer of defense.
**Prevention:** During reviews of static HTML files or templates, always check external URLs for both HTTPS scheme and secure link attributes (`target="_blank" rel="noopener noreferrer"`).

## 2024-04-27 - Relaxed CSP style-src
**Vulnerability:** The Content Security Policy explicitly allowed `'unsafe-inline'` for `style-src`. This makes the application vulnerable to style-based injection attacks (like exfiltrating data via CSS attribute selectors) if an attacker can inject malicious style tags or inline style attributes.
**Learning:** Even a single hardcoded inline `style` attribute in an HTML file often leads developers to broadly allow `'unsafe-inline'` across the entire application's CSP, significantly weakening its defense-in-depth posture.
**Prevention:** Always extract inline styles to external stylesheets (`.css` files) and ensure the CSP `style-src` is restricted to `'self'` or specific trusted origins, strictly avoiding `'unsafe-inline'`.
