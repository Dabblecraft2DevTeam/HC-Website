from playwright.sync_api import sync_playwright

def test_menu_dismissal():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 375, 'height': 667})
        page = context.new_page()
        page.goto('file:///app/index.html')

        menu_toggle = page.locator('.menu-toggle')
        nav_links = page.locator('.nav-links')

        # Test Escape key
        menu_toggle.click()
        assert nav_links.is_visible(), "Menu should be visible after clicking toggle"
        page.keyboard.press('Escape')
        assert not nav_links.is_visible(), "Menu should be hidden after pressing Escape"

        # Check focus is returned
        focus_class = page.evaluate("document.activeElement.className")
        assert "menu-toggle" in focus_class, f"Focus should return to menu-toggle, but was on: {focus_class}"

        # Test click outside
        menu_toggle.click()
        assert nav_links.is_visible(), "Menu should be visible after clicking toggle"
        page.evaluate("document.body.click()") # Click somewhere outside the menu
        assert not nav_links.is_visible(), "Menu should be hidden after clicking outside"

        browser.close()
        print("Menu dismissal test passed!")

if __name__ == "__main__":
    test_menu_dismissal()
