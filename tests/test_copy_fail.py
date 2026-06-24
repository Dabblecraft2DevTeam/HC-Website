from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Not granting clipboard permissions
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        # Mock navigator.clipboard to reject
        page.evaluate("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.reject(new Error("Clipboard permission denied"))
                },
                writable: true,
                configurable: true
            });
        """)

        address_locator = page.locator(".server-address")
        address_locator.wait_for(state="attached")

        # Click to trigger copy
        address_locator.click()

        # Wait a small bit for UI update
        page.wait_for_timeout(100)

        # Verify 'Copy failed!' states
        failed_text = address_locator.text_content().strip()
        failed_aria_label = address_locator.get_attribute("aria-label")
        failed_title = address_locator.get_attribute("title")

        assert failed_text == "Copy failed!", f"Expected 'Copy failed!', got {failed_text}"
        assert failed_aria_label == "Failed to copy server IP address", f"Expected 'Failed to copy server IP address', got {failed_aria_label}"
        assert failed_title == "Copy failed!", f"Expected 'Copy failed!', got {failed_title}"

        # Wait for the timeout to expire (> 2000ms)
        page.wait_for_timeout(2500)

        original_text = "hc.nbz.boats"
        original_aria_label = "Copy server IP address"
        original_title = "Click to copy IP"

        # Verify states reverted to original values
        reverted_text = address_locator.text_content().strip()
        reverted_aria_label = address_locator.get_attribute("aria-label")
        reverted_title = address_locator.get_attribute("title")

        assert reverted_text == original_text, f"Expected {original_text}, got {reverted_text}"
        assert reverted_aria_label == original_aria_label, f"Expected {original_aria_label}, got {reverted_aria_label}"
        assert reverted_title == original_title, f"Expected {original_title}, got {reverted_title}"

        context.close()
        browser.close()
        print("Test test_copy_fail.py passed successfully.")

if __name__ == "__main__":
    run()
