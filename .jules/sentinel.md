## 2024-04-25 - Insecure External Links
**Vulnerability:** External links using `http://` instead of `https://` (specifically on Instagram and TikTok links), exposing users to potential MITM attacks when leaving the site. Furthermore, all external links lacked `target="_blank" rel="noopener noreferrer"`. Missing `rel="noopener noreferrer"` can expose the site to reverse tabnabbing attacks where the newly opened page can maliciously manipulate the originating page via `window.opener`.
**Learning:** Hardcoded links in static HTML files often miss the `rel="noopener noreferrer"` attribute when `target="_blank"` is not explicitly used, but even without it, external links can be used as vectors. Ensuring both HTTPS and secure target attributes is a simple but critical layer of defense.
**Prevention:** During reviews of static HTML files or templates, always check external URLs for both HTTPS scheme and secure link attributes (`target="_blank" rel="noopener noreferrer"`).

## 2024-05-18 - Unsafe Inline CSS
**Vulnerability:** Use of inline `style="..."` attributes required 'unsafe-inline' in Content-Security-Policy style-src. This weak policy could allow an attacker who manages to inject HTML to easily apply arbitrary malicious styles, facilitating attacks like clickjacking or data exfiltration.
**Learning:** Even static sites need strict CSPs. The convenience of inline styles on a single element can compromise the security posture of the entire application by forcing a weakened CSP policy.
**Prevention:** Avoid inline styles. Define all styling in external CSS files via classnames and maintain a strict `style-src 'self'` CSP without 'unsafe-inline'.

## 2024-06-25 - Meta Tag CSP Directives
**Vulnerability:** A static site relying entirely on `<meta>` tags for its Content Security Policy misses out on directives like `frame-ancestors`, `report-uri`, and `sandbox` which are ignored by browsers in `<meta>` tags. Without headers to handle these directives, the site's security posture is inherently weaker, and it lacks protection against attacks like Clickjacking or Mixed Content vulnerabilities if standard defenses are assumed to apply.
**Learning:** For static sites deployed without backend server control, security relies solely on the HTTP `<meta>` equivalent. Because `<meta>` CSP directives do not support `frame-ancestors`, securing the application requires other methods. Crucially, enforcing `upgrade-insecure-requests; block-all-mixed-content;` remains necessary since other mixed-content protections might not be adequately handled in an environment without proper security headers.
**Prevention:** When assessing static sites, always check `<meta>` tag CSP limits. Ensure supported directives like `upgrade-insecure-requests` and `block-all-mixed-content` are present to protect against mixed content and man-in-the-middle attacks, recognizing that these must be configured via supported methods.

## 2026-05-02 - Missing Clickjacking Protection via Meta Tags
**Vulnerability:** The site was entirely vulnerable to clickjacking because `frame-ancestors` is not supported within `<meta>` tags and there is no server configuring Content-Security-Policy or X-Frame-Options HTTP headers.
**Learning:** It is impossible to use `frame-ancestors` in CSP implemented with an HTML `<meta>` tag. Therefore, if a static site is deployed without server-side HTTP headers, it will be vulnerable to clickjacking unless client-side mitigations are implemented.
**Prevention:** Always implement a JavaScript frame-busting script (`if (window.self !== window.top) { window.top.location = window.self.location; }`) in static websites that are unable to configure HTTP response headers.
