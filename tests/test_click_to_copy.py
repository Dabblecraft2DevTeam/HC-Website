from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock navigator.clipboard to prevent DOMException with file:// urls
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.resolve(),
                    readText: () => Promise.resolve('mocked text')
                },
                writable: true,
                configurable: true
            });
        """)

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        # Wait for the click-to-copy element
        server_address = page.locator(".server-address").first
        server_address.wait_for(state="attached")

        # Verify initial state
        initial_title = server_address.get_attribute("title")
        assert initial_title == "Click to copy IP", f"Initial title should be 'Click to copy IP', got '{initial_title}'"

        initial_aria_label = server_address.get_attribute("aria-label")
        assert initial_aria_label == "Copy server IP address", f"Initial aria-label should be 'Copy server IP address', got '{initial_aria_label}'"

        initial_text = server_address.text_content()

        # Click to trigger copy
        server_address.click()

        # Verify state after click
        page.wait_for_function('el => el.textContent === "Copied!"', arg=server_address.evaluate_handle("el => el"))

        copied_title = server_address.get_attribute("title")
        assert copied_title == "Copied!", f"Title should be 'Copied!' after click, got '{copied_title}'"

        copied_aria_label = server_address.get_attribute("aria-label")
        assert copied_aria_label == "Server IP address copied!", f"Aria-label should be 'Server IP address copied!' after click, got '{copied_aria_label}'"

        # Wait for timeout (2000ms + some buffer)
        page.wait_for_timeout(2500)

        # Verify state restored
        restored_title = server_address.get_attribute("title")
        assert restored_title == "Click to copy IP", f"Restored title should be 'Click to copy IP', got '{restored_title}'"

        restored_aria_label = server_address.get_attribute("aria-label")
        assert restored_aria_label == "Copy server IP address", f"Restored aria-label should be 'Copy server IP address', got '{restored_aria_label}'"

        restored_text = server_address.text_content()
        assert restored_text == initial_text, f"Restored text should match initial text"

        browser.close()
        print("Click to copy tests passed successfully.")

if __name__ == "__main__":
    run()
