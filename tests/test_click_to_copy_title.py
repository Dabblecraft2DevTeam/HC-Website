from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Adding permissions to allow clipboard usage without throwing a DOMException
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Determine the absolute path to index.html using the /app directory
        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            # Fallback if not run inside the expected /app environment
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        # Add init script to mock clipboard because we use a file:// URL and it might still throw
        page.add_init_script("""
            Object.defineProperty(navigator, 'clipboard', {
                value: { writeText: () => Promise.resolve() },
                writable: true,
                configurable: true
            });
        """)

        page.goto(f"file://{html_file}")

        # Wait for the first server-address element
        server_address = page.locator(".server-address").first
        server_address.wait_for(state="attached")

        # Verify initial state
        initial_text = server_address.text_content()
        initial_title = server_address.get_attribute("title")
        assert initial_title == "Click to copy IP", f"Expected title to be 'Click to copy IP', got '{initial_title}'"

        # Click the element
        server_address.click()

        # Wait for text to change
        page.wait_for_function(
            "el => el.textContent === 'Copied!'",
            arg=server_address.element_handle()
        )

        # Verify copied state
        copied_text = server_address.text_content()
        copied_title = server_address.get_attribute("title")
        assert copied_text == "Copied!", f"Expected text to be 'Copied!', got '{copied_text}'"
        assert copied_title == "Copied!", f"Expected title to be 'Copied!', got '{copied_title}'"

        # Wait for timeout to revert
        page.wait_for_timeout(2500)

        # Verify reverted state
        reverted_text = server_address.text_content()
        reverted_title = server_address.get_attribute("title")
        assert reverted_text == initial_text, f"Expected text to be '{initial_text}', got '{reverted_text}'"
        assert reverted_title == "Click to copy IP", f"Expected title to be 'Click to copy IP', got '{reverted_title}'"

        browser.close()
        print("Test passed successfully.")

if __name__ == "__main__":
    run()
