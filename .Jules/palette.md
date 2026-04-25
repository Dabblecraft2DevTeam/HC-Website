## 2026-04-25 - Focus-Visible Enhancements for Dark Themes
**Learning:** The static exported website relied entirely on default browser outlines for focus states, which are often invisible against its dark background (#2b2b2b) and custom hover states. Providing explicit `:focus-visible` outlines (like `outline: 2px solid #fff`) ensures high contrast and clarity for keyboard users without disrupting the mouse interaction design.
**Action:** Proactively check dark-themed static sites for sufficient focus indicator contrast and implement `:focus-visible` rather than relying on browser defaults.
