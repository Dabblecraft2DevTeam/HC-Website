## 2026-04-25 - Focus-Visible Enhancements for Dark Themes
**Learning:** The static exported website relied entirely on default browser outlines for focus states, which are often invisible against its dark background (#2b2b2b) and custom hover states. Providing explicit `:focus-visible` outlines (like `outline: 2px solid #fff`) ensures high contrast and clarity for keyboard users without disrupting the mouse interaction design.
**Action:** Proactively check dark-themed static sites for sufficient focus indicator contrast and implement `:focus-visible` rather than relying on browser defaults.

## 2024-04-27 - Accessible Click-to-Copy for Static Text
**Learning:** Making static text elements (like an IP address or code snippet) interactive for click-to-copy functionality requires adding `role="button"` and `tabindex="0"`, along with both `click` and `keydown` event listeners (for Space/Enter) to ensure they are accessible to keyboard and screen reader users. Visual feedback (e.g. temporary text change to "Copied!" and `cursor: pointer`) is essential.
**Action:** When converting static text to interactive copying elements, always apply ARIA button roles, `tabindex`, keyboard event listeners, and clear visual feedback states.
## 2024-11-20 - Adding Skip-to-Content Link
**Learning:** Added a "Skip to main content" link that is visually hidden and appears on focus. This pattern enables keyboard users to bypass repetitive navigation elements.
**Action:** Always ensure hidden elements like skip links are made visible on `:focus` to ensure they are actionable and noticeable for keyboard-only users.
