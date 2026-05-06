from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport
        context = browser.new_context(viewport={'width': 375, 'height': 667})
        page = context.new_page()

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        page.goto(f"file://{html_file}")

        menu_toggle = page.locator(".menu-toggle")
        nav_links = page.locator(".nav-links")

        print("Initial state:")
        print("Menu toggle is visible:", menu_toggle.is_visible())
        print("Nav links is visible:", nav_links.is_visible())

        # Click menu toggle
        menu_toggle.click()
        page.wait_for_timeout(500)

        print("\nAfter click:")
        print("Nav links is visible:", nav_links.is_visible())
        print("aria-expanded:", menu_toggle.get_attribute("aria-expanded"))
        print("aria-label:", menu_toggle.get_attribute("aria-label"))

        # Press Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        print("\nAfter Escape:")
        print("Nav links is visible:", nav_links.is_visible())
        print("aria-expanded:", menu_toggle.get_attribute("aria-expanded"))

        assert not nav_links.is_visible(), "Nav links should be hidden after pressing Escape"
        assert menu_toggle.get_attribute("aria-expanded") == "false", "Menu toggle should have aria-expanded='false' after pressing Escape"

        # Verify focus is returned to menu toggle
        focused_element = page.evaluate("document.activeElement.className")
        print("Focused element class:", focused_element)
        assert "menu-toggle" in focused_element, "Menu toggle should be focused after pressing Escape"

        # Click menu toggle again
        menu_toggle.click()
        page.wait_for_timeout(500)
        assert nav_links.is_visible(), "Nav links should be visible after clicking menu toggle"

        # Click outside menu
        page.mouse.click(0, 0)
        page.wait_for_timeout(500)

        print("\nAfter click outside:")
        print("Nav links is visible:", nav_links.is_visible())
        print("aria-expanded:", menu_toggle.get_attribute("aria-expanded"))

        assert not nav_links.is_visible(), "Nav links should be hidden after clicking outside"
        assert menu_toggle.get_attribute("aria-expanded") == "false", "Menu toggle should have aria-expanded='false' after clicking outside"

        # Click menu toggle again
        menu_toggle.click()
        page.wait_for_timeout(500)
        assert nav_links.is_visible(), "Nav links should be visible after clicking menu toggle"

        # Click inside menu (on a non-link area if possible, or prevent default)
        page.evaluate("document.querySelector('.nav-links').addEventListener('click', e => e.preventDefault())")
        nav_links.click()
        page.wait_for_timeout(500)

        print("\nAfter click inside:")
        print("Nav links is visible:", nav_links.is_visible())
        print("aria-expanded:", menu_toggle.get_attribute("aria-expanded"))

        assert nav_links.is_visible(), "Nav links should still be visible after clicking inside"
        assert menu_toggle.get_attribute("aria-expanded") == "true", "Menu toggle should have aria-expanded='true' after clicking inside"

        browser.close()

if __name__ == "__main__":
    run()
