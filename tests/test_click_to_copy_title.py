from playwright.sync_api import sync_playwright

def test_click_to_copy_title():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Grant clipboard permissions for tests
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock the clipboard API
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: { writeText: () => Promise.resolve() },
                writable: true,
                configurable: true
            });
        """)

        # Start a local HTTP server in a separate terminal or serve files appropriately
        # Assuming we can just test from the local file using file://
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = f"file://{base_dir}/index.html"

        page.goto(file_path)

        # Find the server address element
        address_element = page.locator('.server-address').first

        # Check initial title
        assert address_element.get_attribute('title') == 'Click to copy IP'

        # Click the element
        address_element.click()

        # Check the title is updated to 'Copied!'
        assert address_element.get_attribute('title') == 'Copied!'

        browser.close()

if __name__ == "__main__":
    test_click_to_copy_title()
    print("test_click_to_copy_title passed!")
