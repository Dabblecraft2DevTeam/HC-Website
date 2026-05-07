from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport to show the menu toggle
        context = browser.new_context(viewport={'width': 375, 'height': 667})
        page = context.new_page()

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        menu_toggle = page.locator(".menu-toggle")
        nav_links = page.locator(".nav-links")

        # Initial state: closed
        assert not nav_links.evaluate("el => el.classList.contains('active')"), "Menu should be closed initially"
        assert menu_toggle.get_attribute('aria-expanded') == 'false', "aria-expanded should be false initially"

        # Open the menu
        menu_toggle.click()

        # Verify state: opened
        page.wait_for_function('document.querySelector(".nav-links").classList.contains("active")')
        assert nav_links.evaluate("el => el.classList.contains('active')"), "Menu should be open after click"
        assert menu_toggle.get_attribute('aria-expanded') == 'true', "aria-expanded should be true after click"

        # Close with Escape key
        page.keyboard.press("Escape")

        # Verify state: closed
        page.wait_for_function('!document.querySelector(".nav-links").classList.contains("active")')
        assert not nav_links.evaluate("el => el.classList.contains('active')"), "Menu should be closed after Escape"
        assert menu_toggle.get_attribute('aria-expanded') == 'false', "aria-expanded should be false after Escape"

        # Verify focus is returned to the menu toggle
        focused_element_classes = page.evaluate("document.activeElement.className")
        assert "menu-toggle" in focused_element_classes, "Focus should return to the menu toggle"

        browser.close()
        print("Tests passed successfully.")

if __name__ == "__main__":
    run()
