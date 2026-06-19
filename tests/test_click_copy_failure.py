from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Without clipboard permissions it will fail
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        address_locator = page.locator(".server-address").first
        address_locator.wait_for(state="attached")

        original_text = address_locator.text_content().strip()
        original_aria_label = address_locator.get_attribute("aria-label")
        original_title = address_locator.get_attribute("title")

        address_locator.click()
        page.wait_for_timeout(100)

        copied_text = address_locator.text_content().strip()
        copied_aria_label = address_locator.get_attribute("aria-label")
        copied_title = address_locator.get_attribute("title")

        assert copied_text == "Copy failed!", f"Expected 'Copy failed!', got {copied_text}"
        assert copied_aria_label == "Copy failed!", f"Expected 'Copy failed!', got {copied_aria_label}"
        assert copied_title == "Copy failed!", f"Expected 'Copy failed!', got {copied_title}"

        # Simulate rapid successive clicks
        address_locator.click()
        page.wait_for_timeout(50)
        address_locator.click()
        page.wait_for_timeout(50)

        page.wait_for_timeout(2500)

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
