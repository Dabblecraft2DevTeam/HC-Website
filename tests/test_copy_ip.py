from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions for testing copy to clipboard
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock clipboard to prevent DOMExceptions in headless browsers
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

        # Wait for the server address element
        server_address = page.locator(".server-address").first
        server_address.wait_for(state="attached")

        # Verify initial state
        initial_text = server_address.text_content()
        initial_aria_label = server_address.get_attribute("aria-label")
        initial_title = server_address.get_attribute("title")

        assert initial_text == "hc.nbz.boats", f"Expected initial text to be 'hc.nbz.boats', got {initial_text}"
        assert initial_aria_label == "Copy server IP address", f"Expected initial aria-label, got {initial_aria_label}"
        assert initial_title == "Click to copy IP", f"Expected initial title, got {initial_title}"

        # Click to trigger copy event
        server_address.click()

        # Verify 'Copied!' state
        page.wait_for_function('el => el.textContent === "Copied!"', arg=server_address.element_handle())

        copied_text = server_address.text_content()
        copied_aria_label = server_address.get_attribute("aria-label")
        copied_title = server_address.get_attribute("title")

        assert copied_text == "Copied!", f"Expected text to be 'Copied!', got {copied_text}"
        assert copied_aria_label == "Server IP address copied!", f"Expected copied aria-label, got {copied_aria_label}"
        assert copied_title == "Copied!", f"Expected copied title, got {copied_title}"

        # Wait for restoration (timeout is 2000ms)
        page.wait_for_timeout(2500)

        # Verify restored state
        restored_text = server_address.text_content()
        restored_aria_label = server_address.get_attribute("aria-label")
        restored_title = server_address.get_attribute("title")

        assert restored_text == initial_text, f"Expected restored text to be '{initial_text}', got {restored_text}"
        assert restored_aria_label == initial_aria_label, f"Expected restored aria-label to be '{initial_aria_label}', got {restored_aria_label}"
        assert restored_title == initial_title, f"Expected restored title to be '{initial_title}', got {restored_title}"

        browser.close()
        print("Tests passed successfully.")

if __name__ == "__main__":
    run()
