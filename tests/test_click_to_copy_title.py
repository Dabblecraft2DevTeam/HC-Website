from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions for testing
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock navigator.clipboard to prevent DOMExceptions in tests
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: { writeText: () => Promise.resolve() },
                writable: true,
                configurable: true
            });
        """)

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        server_address = page.locator(".server-address").first
        server_address.wait_for(state="attached")

        # Verify initial title
        initial_title = server_address.get_attribute("title")
        assert initial_title == "Click to copy IP", f"Initial title should be 'Click to copy IP', got {initial_title}"

        # Click to trigger copy
        server_address.click()

        # Verify updated title
        updated_title = server_address.get_attribute("title")
        assert updated_title == "Copied!", f"Title should be 'Copied!' immediately after click, got {updated_title}"

        # Wait for the timeout (2000ms + some buffer)
        page.wait_for_timeout(2500)

        # Verify title reverts back
        reverted_title = server_address.get_attribute("title")
        assert reverted_title == "Click to copy IP", f"Title should revert to 'Click to copy IP' after timeout, got {reverted_title}"

        browser.close()
        print("Test passed successfully.")

if __name__ == "__main__":
    run()