## 2026-04-25 - Focus-Visible Enhancements for Dark Themes
**Learning:** The static exported website relied entirely on default browser outlines for focus states, which are often invisible against its dark background (#2b2b2b) and custom hover states. Providing explicit `:focus-visible` outlines (like `outline: 2px solid #fff`) ensures high contrast and clarity for keyboard users without disrupting the mouse interaction design.
**Action:** Proactively check dark-themed static sites for sufficient focus indicator contrast and implement `:focus-visible` rather than relying on browser defaults.

## 2024-04-27 - Accessible Click-to-Copy for Static Text
**Learning:** Making static text elements (like an IP address or code snippet) interactive for click-to-copy functionality requires adding `role="button"` and `tabindex="0"`, along with both `click` and `keydown` event listeners (for Space/Enter) to ensure they are accessible to keyboard and screen reader users. Visual feedback (e.g. temporary text change to "Copied!" and `cursor: pointer`) is essential.
**Action:** When converting static text to interactive copying elements, always apply ARIA button roles, `tabindex`, keyboard event listeners, and clear visual feedback states.

## 2024-05-18 - Skip-to-Content Link for Accessibility
**Learning:** Adding a "skip to main content" link is a critical accessibility enhancement for users navigating with a keyboard or screen reader. The link must be technically off-screen when inactive (e.g., using `transform: translateY(-100%)`) but become fully visible upon receiving `:focus` or `:focus-visible`. Additionally, the target element (usually `<main>`) must have `id="main"` and `tabindex="-1"` to properly capture focus when jumped to, while CSS should suppress its default focus outline (`outline: none`) so it remains visually clean.
**Action:** When auditing static or standard HTML pages, immediately verify the existence of a skip link. If missing, implement one immediately after the opening `<body>` tag, target it to a `<main tabindex="-1">` element, and ensure smooth visual transition into the viewport upon focus.
