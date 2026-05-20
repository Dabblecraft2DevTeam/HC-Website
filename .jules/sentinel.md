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

## 2024-06-25 - Meta Tag CSP Directives
**Vulnerability:** A static site relying entirely on `<meta>` tags for its Content Security Policy misses out on directives like `frame-ancestors`, `report-uri`, and `sandbox` which are ignored by browsers in `<meta>` tags. Without headers to handle these directives, the site's security posture is inherently weaker, and it lacks protection against attacks like Clickjacking or Mixed Content vulnerabilities if standard defenses are assumed to apply.
**Learning:** For static sites deployed without backend server control, security relies solely on the HTTP `<meta>` equivalent. Because `<meta>` CSP directives do not support `frame-ancestors`, securing the application requires other methods. Crucially, enforcing `upgrade-insecure-requests; block-all-mixed-content;` remains necessary since other mixed-content protections might not be adequately handled in an environment without proper security headers.
**Prevention:** When assessing static sites, always check `<meta>` tag CSP limits. Ensure supported directives like `upgrade-insecure-requests` and `block-all-mixed-content` are present to protect against mixed content and man-in-the-middle attacks, recognizing that these must be configured via supported methods.

## 2026-05-02 - Missing Clickjacking Protection via Meta Tags
**Vulnerability:** The site was entirely vulnerable to clickjacking because `frame-ancestors` is not supported within `<meta>` tags and there is no server configuring Content-Security-Policy or X-Frame-Options HTTP headers.
**Learning:** It is impossible to use `frame-ancestors` in CSP implemented with an HTML `<meta>` tag. Therefore, if a static site is deployed without server-side HTTP headers, it will be vulnerable to clickjacking unless client-side mitigations are implemented.
**Prevention:** Always implement a JavaScript frame-busting script (`if (window.self !== window.top) { window.top.location = window.self.location; }`) in static websites that are unable to configure HTTP response headers.

## 2026-05-04 - Hide-First Anti-Clickjacking
**Vulnerability:** The existing frame-busting script (`window.top.location = window.self.location`) was vulnerable because an attacker can embed the page in an iframe with the `sandbox="allow-scripts"` attribute, which prevents the frame from navigating the top-level window. This completely bypasses the traditional JavaScript-based frame-busting defense.
**Learning:** Traditional JS frame-busting can be trivially bypassed using HTML5 sandbox attributes. A "hide-first" approach is more robust: use a strict CSS class (`.anti-clickjack { display: none !important; }`) to hide the page content by default, and only remove it via JavaScript if `window.self === window.top`. Since the CSP `style-src 'self'` prevents attackers from overriding this with inline styles, the page remains securely hidden when embedded.
**Prevention:** Always use the hide-first pattern combined with a strict `style-src` CSP to implement client-side anti-clickjacking defenses instead of relying purely on frame navigation.

## 2026-10-18 - Frame-Busting Unhandled Exceptions Leakage
**Vulnerability:** When a page utilizes traditional JavaScript frame-busting logic (`window.top.location = window.self.location`) and is embedded in a highly restrictive iframe (e.g., one without the `allow-top-navigation` sandbox attribute), attempting to read or write to `window.top.location` results in a cross-origin `DOMException` or security error. If unhandled, this exception can leak stack traces and internal execution contexts to the browser console or monitoring tools, potentially exposing sensitive implementation details.
**Learning:** Security mechanisms like frame-busting can themselves become vectors for information leakage if their failure states are not accounted for. Code executing in untrusted or potentially hostile embedding contexts must assume that browser security policies (like CORS or sandboxing) might forcefully block its execution, causing it to throw errors.
**Prevention:** When implementing or modifying frame-busting logic, always wrap it in a `try...catch` block to safely swallow or generically handle `DOMException`s, preventing stack trace leakage in restrictive sandboxes.

## 2026-10-18 - Client-Side Error Suppression Security Theater
**Vulnerability:** An attempt was made to suppress raw error objects in `console.error` (e.g., from a failed clipboard `DOMException`) to prevent "stack trace leakage".
**Learning:** Client-side browser errors do not contain sensitive backend internals or server data. Suppressing them provides absolutely zero security benefit and actively worsens frontend observability and debugging capabilities. This constitutes "security theater."
**Prevention:** Never suppress client-side error objects under the guise of security unless the error message explicitly contains embedded secrets (e.g., tokens inadvertently included in the error string).

## 2026-10-18 - Restricting Iframe and Worker Sources in Meta CSP
**Vulnerability:** A static site utilizing `<meta>` tags for its CSP allowed `frame-src`, `child-src`, and `worker-src` to fall back to `default-src 'self'`. This allowed the page to potentially embed same-origin iframes or spawn web workers, increasing the attack surface if an injection vulnerability were discovered.
**Learning:** Even if `frame-ancestors` (which protects *against* being embedded) is unsupported in `<meta>` tags, restricting what the page itself can embed is still highly effective. Setting unused resource directives to `'none'` instead of relying on the default fallback is a simple and powerful defense-in-depth measure.
**Prevention:** Always append `frame-src 'none'; child-src 'none'; worker-src 'none';` to `<meta>` CSP tags in static sites unless the site explicitly requires embedding iframes or spawning workers.
