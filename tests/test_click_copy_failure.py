from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions for testing
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        # Mock navigator.clipboard with a rejection
        page.evaluate("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.reject(new Error("Permission denied"))
                },
                writable: true,
                configurable: true
            });
        """)

        address_locator = page.locator(".server-address").first
        address_locator.wait_for(state="attached")

        # Verify initial states
        original_text = address_locator.text_content().strip()
        original_aria_label = address_locator.get_attribute("aria-label")
        original_title = address_locator.get_attribute("title")

        # Click to trigger copy failure
        address_locator.click()

        # Wait a small bit for UI update
        page.wait_for_timeout(100)

        # Verify 'Copy failed!' states
        failed_text = address_locator.text_content().strip()
        failed_aria_label = address_locator.get_attribute("aria-label")
        failed_title = address_locator.get_attribute("title")

        assert failed_text == "Copy failed!", f"Expected 'Copy failed!', got {failed_text}"
        assert failed_aria_label == "Copy failed!", f"Expected 'Copy failed!', got {failed_aria_label}"
        assert failed_title == "Copy failed!", f"Expected 'Copy failed!', got {failed_title}"

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
        print("Test test_click_copy_failure.py passed successfully.")

if __name__ == "__main__":
    run()
