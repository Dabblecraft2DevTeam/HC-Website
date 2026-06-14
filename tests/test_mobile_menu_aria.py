from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 375, 'height': 667})
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        menu_toggle = page.locator(".menu-toggle")
        nav_links = page.locator(".nav-links")

        menu_toggle.wait_for(state="attached")
        nav_links.wait_for(state="attached")

        # Initial state check
        assert menu_toggle.get_attribute("aria-expanded") == "false", "Initial aria-expanded should be false"
        assert menu_toggle.get_attribute("aria-controls") == "nav-menu", "aria-controls should be nav-menu"
        assert nav_links.get_attribute("id") == "nav-menu", "nav-links should have id nav-menu"

        # Toggle state check
        menu_toggle.click()
        page.wait_for_timeout(100) # Give js some time
        assert menu_toggle.get_attribute("aria-expanded") == "true", "aria-expanded should be true after click"

        menu_toggle.click()
        page.wait_for_timeout(100)
        assert menu_toggle.get_attribute("aria-expanded") == "false", "aria-expanded should be false after close"

        context.close()
        browser.close()
        print("Test test_mobile_menu_aria.py passed successfully.")

if __name__ == "__main__":
    run()
