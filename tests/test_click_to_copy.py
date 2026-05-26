from playwright.sync_api import sync_playwright
import os
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mocking navigator.clipboard as headless browsers block clipboard access
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

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

        # Locate the server address element
        server_address = page.locator(".server-address").first
        server_address.wait_for(state="attached")

        # Verify initial states
        assert server_address.text_content() == "hc.nbz.boats", "Initial text should be hc.nbz.boats"
        assert server_address.get_attribute("title") == "Click to copy IP", "Initial title should be 'Click to copy IP'"

        # Click the element
        server_address.click()

        # Verify updated states (Copied!)
        assert server_address.text_content() == "Copied!", "Text should update to 'Copied!' after click"
        assert server_address.get_attribute("title") == "Copied!", "Title should update to 'Copied!' after click"

        # Wait for the timeout to revert states
        time.sleep(2.5) # The timeout in main.js is 2000ms

        # Verify reverted states
        assert server_address.text_content() == "hc.nbz.boats", "Text should revert to hc.nbz.boats after timeout"
        assert server_address.get_attribute("title") == "Click to copy IP", "Title should revert to 'Click to copy IP' after timeout"

        browser.close()
        print("Test test_click_to_copy passed successfully.")

if __name__ == "__main__":
    run()
