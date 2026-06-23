from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Deny clipboard permissions for testing error state
        context = browser.new_context(permissions=[])
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        # Mock navigator.clipboard to reject
        page.evaluate("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.reject(new Error("Permission denied"))
                },
                writable: true,
                configurable: true
            });
        """)

        address_locator = page.locator(".server-address")
        address_locator.wait_for(state="attached")

        original_text = address_locator.text_content().strip()

        # Click to trigger copy
        address_locator.click()

        # Wait a small bit for UI update
        page.wait_for_timeout(100)

        # Verify 'Copy failed!' states
        copied_text = address_locator.text_content().strip()
        copied_aria_label = address_locator.get_attribute("aria-label")
        copied_title = address_locator.get_attribute("title")

        assert copied_text == "Copy failed!", f"Expected 'Copy failed!', got {copied_text}"
        assert copied_aria_label == "Failed to copy server IP address", f"Expected 'Failed to copy server IP address', got {copied_aria_label}"
        assert copied_title == "Copy failed!", f"Expected 'Copy failed!', got {copied_title}"

        # Wait for the timeout to expire (> 2000ms)
        page.wait_for_timeout(2500)

        # Verify states reverted to original values
        reverted_text = address_locator.text_content().strip()

        assert reverted_text == original_text, f"Expected {original_text}, got {reverted_text}"

        context.close()
        browser.close()
        print("Test test_click_copy_error.py passed successfully.")

if __name__ == "__main__":
    run()
