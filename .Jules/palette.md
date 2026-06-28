## 2026-04-25 - Focus-Visible Enhancements for Dark Themes
**Learning:** The static exported website relied entirely on default browser outlines for focus states, which are often invisible against its dark background (#2b2b2b) and custom hover states. Providing explicit `:focus-visible` outlines (like `outline: 2px solid #fff`) ensures high contrast and clarity for keyboard users without disrupting the mouse interaction design.
**Action:** Proactively check dark-themed static sites for sufficient focus indicator contrast and implement `:focus-visible` rather than relying on browser defaults.

## 2024-04-27 - Accessible Click-to-Copy for Static Text
**Learning:** Making static text elements (like an IP address or code snippet) interactive for click-to-copy functionality requires adding `role="button"` and `tabindex="0"`, along with both `click` and `keydown` event listeners (for Space/Enter) to ensure they are accessible to keyboard and screen reader users. Visual feedback (e.g. temporary text change to "Copied!" and `cursor: pointer`) is essential.
**Action:** When converting static text to interactive copying elements, always apply ARIA button roles, `tabindex`, keyboard event listeners, and clear visual feedback states.

## 2026-05-02 - Sticky Headers and Skip Links
**Learning:** When implementing "skip to content" links on a site with a sticky or fixed header, the targeted element (usually `<main>`) needs CSS `scroll-margin-top` to prevent the content from being hidden underneath the header when the skip link is activated and the browser scrolls to the target.
**Action:** Always verify the interaction between skip-to-content anchor targets and sticky headers, adding `scroll-margin-top` as needed.

## 2024-11-20 - Dynamic Text Updates in Custom Controls
**Learning:** When a custom interactive element updates its text content to provide feedback (e.g., changing "hc.nbz.boats" to "Copied!"), a static `aria-label` will override the text content, preventing screen readers from announcing the change even if `aria-live="polite"` is set.
**Action:** Always dynamically update the `aria-label` alongside the visual text content when providing interaction feedback, or avoid static `aria-labels` when the text content itself is already descriptive. Ensure `[role="button"]` elements receive the same focus-visible styles as native buttons.

## 2024-05-24 - Interactive Text Affordances & Layout Stability
**Learning:** Programmatically adding `role="button"` to inline text for features like click-to-copy is insufficient for UX if visual button affordances are missing. Furthermore, dynamically changing the text (e.g., from an IP address to "Copied!") causes jarring layout shifts if the inline element lacks a fixed minimum width.
**Action:** When implementing click-to-copy or similar inline dynamic text interactions, always add visual button affordances (background, padding, border-radius, hover/active states) and a fixed `min-width` with centered text to ensure layout stability during state changes.
## 2025-05-09 - Safely Dismissing Mobile Menus via Outside Clicks
**Learning:** Using `e.stopPropagation()` on toggle buttons to prevent document click handlers from firing is risky and can block legitimate global events. Furthermore, checking outside clicks must account for the toggle trigger itself to avoid reopening behavior immediately after closing.
**Action:** When implementing outside click dismissal, attach a document-level click listener and conditionally close only if `!trigger.contains(e.target) && !menu.contains(e.target)`, ensuring both the trigger button and the menu itself are excluded from the "outside" area.

## 2026-05-19 - Communicating Context Switches for External Links
**Learning:** When external links (`target="_blank"`) lack visual cues (like an external link icon) and adding new CSS classes or inline styles is prohibited by strict boundaries (like a `style-src 'self'` CSP and "no custom CSS" rule), screen reader users are left unaware of the context switch.
**Action:** Use a combination of `aria-label="Link Text (opens in a new tab)"` to inform screen readers and `title="Opens in a new tab"` to provide a native tooltip for sighted mouse users, improving predictability and adhering to WCAG 3.2.5 without requiring any custom CSS.

## 2026-05-19 - Click-to-Copy Tooltip Synchronization and State Regression
**Learning:** When implementing click-to-copy functionality on an element that uses a native `title` attribute for tooltip guidance (e.g., "Click to copy IP"), failing to update the `title` to "Copied!" alongside the `aria-label` and visible text leaves sighted mouse users with confusing, stale feedback. Furthermore, caching original attributes (like `title` and `aria-label`) *inside* the event listener before temporarily modifying them causes "state regression" where rapid, successive interactions permanently overwrite the original cached values with the temporary ones.
**Action:** Always dynamically sync `title` attributes with visual text and `aria-label` changes to provide consistent visual feedback for mouse interactions. To prevent state regressions from rapid interactions, always cache original attribute values outside the event listener during initialization, using `.getAttribute()` and conditionally restoring or removing them with `.removeAttribute()`.

## 2026-06-10 - Initial ARIA States for Mobile Menus
**Learning:** Relying purely on JavaScript to inject initial `aria-expanded` and link toggle buttons to menus dynamically leaves screen readers without crucial context before execution or if JS fails.
**Action:** Hardcode the initial `aria-expanded="false"` state and explicit `aria-controls` bindings directly in the HTML to ensure immediate screen reader accessibility for custom navigation toggles.

## 2026-06-28 - Accessible Error Feedback for Clipboard Rejections
**Learning:** When implementing click-to-copy functionality using the Clipboard API, silently logging promise rejections to the console fails to communicate permission or context failures to the user.
**Action:** Handle promise rejections by providing temporary visual and ARIA error feedback (e.g., changing text, title, and aria-label to 'Copy failed!') to clearly communicate the failure state, reverting to original attributes after a timeout.
