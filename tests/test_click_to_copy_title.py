from playwright.sync_api import sync_playwright
import os
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock navigator.clipboard to prevent DOMExceptions
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.resolve()
                },
                writable: true,
                configurable: true
            });
        """)

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        # Wait for the element
        ip_element = page.locator(".server-address").first
        ip_element.wait_for(state="attached")

        # Verify initial state
        assert ip_element.get_attribute("title") == "Click to copy IP", "Initial title is incorrect"
        assert ip_element.text_content() == "hc.nbz.boats", "Initial text is incorrect"
        assert ip_element.get_attribute("aria-label") == "Copy server IP address", "Initial aria-label is incorrect"

        # Click to trigger copy
        ip_element.click()

        # Wait for text to update without using wait_for_function string evaluation which violates CSP
        page.locator(".server-address:has-text('Copied!')").first.wait_for(state="attached", timeout=3000)

        # Verify updated state
        assert ip_element.get_attribute("title") == "Copied!", "Title was not updated correctly after click"
        assert ip_element.text_content() == "Copied!", "Text was not updated correctly after click"
        assert ip_element.get_attribute("aria-label") == "Server IP address copied!", "Aria-label was not updated correctly after click"

        # Wait for the timeout to revert the state (2000ms)
        page.locator(".server-address:has-text('hc.nbz.boats')").first.wait_for(state="attached", timeout=3000)

        # Verify reverted state
        assert ip_element.get_attribute("title") == "Click to copy IP", "Title did not revert correctly"
        assert ip_element.text_content() == "hc.nbz.boats", "Text did not revert correctly"
        assert ip_element.get_attribute("aria-label") == "Copy server IP address", "Aria-label did not revert correctly"

        context.close()
        browser.close()
        print("Test passed: Click-to-copy title sync works correctly.")

if __name__ == "__main__":
    run()
