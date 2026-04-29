## 2024-04-25 - Insecure External Links
**Vulnerability:** External links using `http://` instead of `https://` (specifically on Instagram and TikTok links), exposing users to potential MITM attacks when leaving the site. Furthermore, all external links lacked `target="_blank" rel="noopener noreferrer"`. Missing `rel="noopener noreferrer"` can expose the site to reverse tabnabbing attacks where the newly opened page can maliciously manipulate the originating page via `window.opener`.
**Learning:** Hardcoded links in static HTML files often miss the `rel="noopener noreferrer"` attribute when `target="_blank"` is not explicitly used, but even without it, external links can be used as vectors. Ensuring both HTTPS and secure target attributes is a simple but critical layer of defense.
**Prevention:** During reviews of static HTML files or templates, always check external URLs for both HTTPS scheme and secure link attributes (`target="_blank" rel="noopener noreferrer"`).

## 2024-05-18 - Unsafe Inline CSS
**Vulnerability:** Use of inline `style="..."` attributes required 'unsafe-inline' in Content-Security-Policy style-src. This weak policy could allow an attacker who manages to inject HTML to easily apply arbitrary malicious styles, facilitating attacks like clickjacking or data exfiltration.
**Learning:** Even static sites need strict CSPs. The convenience of inline styles on a single element can compromise the security posture of the entire application by forcing a weakened CSP policy.
**Prevention:** Avoid inline styles. Define all styling in external CSS files via classnames and maintain a strict `style-src 'self'` CSP without 'unsafe-inline'.

## 2026-04-29 - Unsupported CSP Meta Directives
**Vulnerability:** Adding `frame-ancestors` directive to `<meta http-equiv="Content-Security-Policy">`. Although Clickjacking is a threat, this method is ineffective as browsers explicitly ignore `frame-ancestors` (and `report-uri`, `sandbox`) when delivered via a `<meta>` tag.
**Learning:** When securing static sites without HTTP response header access, verify which CSP directives are actually supported by the `<meta>` tag. Instead, we can enhance the CSP with supported directives like `upgrade-insecure-requests`.
**Prevention:** Always cross-reference the allowed delivery methods for CSP directives before attempting to implement them in a `<meta>` tag.
