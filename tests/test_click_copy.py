from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions for testing
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # We'll use http server to avoid cross-origin / file:// issues with clipboard
        # and mocking the clipboard API for robust testing.
        page.goto("http://localhost:8000/index.html")

        # Mock navigator.clipboard
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.resolve()
                },
                writable: true,
                configurable: true
            });
        """)

        address_locator = page.locator(".server-address")
        address_locator.wait_for(state="attached")

        # Verify initial states
        original_text = address_locator.text_content().strip()
        original_aria_label = address_locator.get_attribute("aria-label")
        original_title = address_locator.get_attribute("title")

        assert original_text == "hc.nbz.boats", f"Expected 'hc.nbz.boats', got {original_text}"
        assert original_aria_label == "Copy server IP address", f"Expected 'Copy server IP address', got {original_aria_label}"
        assert original_title == "Click to copy IP", f"Expected 'Click to copy IP', got {original_title}"

        # Click to trigger copy
        address_locator.click()

        # Wait a small bit for UI update
        page.wait_for_timeout(100)

        # Verify 'Copied!' states
        copied_text = address_locator.text_content().strip()
        copied_aria_label = address_locator.get_attribute("aria-label")
        copied_title = address_locator.get_attribute("title")

        assert copied_text == "Copied!", f"Expected 'Copied!', got {copied_text}"
        assert copied_aria_label == "Server IP address copied!", f"Expected 'Server IP address copied!', got {copied_aria_label}"
        assert copied_title == "Copied!", f"Expected 'Copied!', got {copied_title}"

        # Simulate rapid successive user clicks to test state regression (spamming)
        address_locator.click()
        page.wait_for_timeout(50)
        address_locator.click()
        page.wait_for_timeout(50)

        # Wait for the timeout to expire (> 2000ms)
        page.wait_for_timeout(2500)

        # Verify states reverted to original values
        reverted_text = address_locator.text_content().strip()
        reverted_aria_label = address_locator.get_attribute("aria-label")
        reverted_title = address_locator.get_attribute("title")

        assert reverted_text == original_text, f"Expected {original_text}, got {reverted_text}"
        assert reverted_aria_label == original_aria_label, f"Expected {original_aria_label}, got {reverted_aria_label}"
        assert reverted_title == original_title, f"Expected {original_title}, got {reverted_title}"

        context.close()
        browser.close()
        print("Test test_click_copy.py passed successfully.")

if __name__ == "__main__":
    run()