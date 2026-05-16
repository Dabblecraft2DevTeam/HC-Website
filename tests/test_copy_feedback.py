from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard-write permissions explicitly, though we will also mock it
        context = browser.new_context(permissions=["clipboard-write"])
        page = context.new_page()

        # Mock navigator.clipboard to bypass restrictions in headless environments
        # using Object.defineProperty as per memory instructions
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

        # Find the server address element
        server_address = page.locator(".server-address")
        server_address.wait_for(state="attached")

        # Verify initial state
        assert "copied" not in server_address.get_attribute("class"), "Element should not have copied class initially"

        # Click to trigger copy
        server_address.click()

        # Verify the copied class is added
        page.wait_for_function('document.querySelector(".server-address").classList.contains("copied")')
        assert "copied" in server_address.get_attribute("class"), "Element should have copied class after click"

        # Wait for timeout to expire (2000ms in JS, we wait a bit more)
        page.wait_for_timeout(2500)

        # Verify the copied class is removed
        assert "copied" not in server_address.get_attribute("class"), "Element should not have copied class after timeout"

        browser.close()
        print("Test passed: Click-to-copy explicit visual feedback functions correctly.")

if __name__ == "__main__":
    run()
