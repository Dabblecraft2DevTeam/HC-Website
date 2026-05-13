from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Mock clipboard since headless environments usually block it
        page.add_init_script("navigator.clipboard.writeText = async (text) => {};")

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        address = page.locator(".server-address").first

        # Verify initial state
        assert address.text_content().strip() == "hc.nbz.boats", "Initial text should be the server address"
        assert "copied" not in address.get_attribute("class"), "Initial class should not contain 'copied'"

        box_before = address.bounding_box()

        # Click to trigger copy
        address.click()

        # Give it a short moment for DOM updates
        page.wait_for_timeout(100)

        # Verify state after click
        assert address.text_content().strip() == "Copied!", "Text should change to 'Copied!'"
        assert "copied" in address.get_attribute("class"), "Class should contain 'copied' for visual feedback"

        # Verify no layout shift occurred
        box_after = address.bounding_box()
        assert box_before["width"] == box_after["width"], "Width should remain constant to avoid layout shift"
        assert box_before["height"] == box_after["height"], "Height should remain constant to avoid layout shift"

        # Wait for timeout to expire and verify it resets
        page.wait_for_timeout(2100)
        assert address.text_content().strip() == "hc.nbz.boats", "Text should revert after timeout"
        assert "copied" not in address.get_attribute("class"), "Class 'copied' should be removed after timeout"

        browser.close()
        print("Click to copy test passed successfully.")

if __name__ == "__main__":
    run()
