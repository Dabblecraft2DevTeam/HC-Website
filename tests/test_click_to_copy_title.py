from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Grant clipboard permissions for testing
        context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Determine the absolute path to index.html using the /app directory
        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        # Mock clipboard for file:// urls where it might still fail
        page.add_init_script("Object.defineProperty(navigator, 'clipboard', { value: { writeText: () => Promise.resolve() }, writable: true, configurable: true });")

        # Find the server address element
        address_element = page.locator(".server-address").first
        address_element.wait_for(state="attached")

        # Verify initial title
        title_before = address_element.get_attribute("title")
        assert title_before == "Click to copy IP", f"Initial title should be 'Click to copy IP', got {title_before}"

        # Click the element
        address_element.click()

        # Verify the title changed to Copied!
        page.wait_for_function('el => el.getAttribute("title") === "Copied!"', arg=address_element.element_handle())
        title_after = address_element.get_attribute("title")
        assert title_after == "Copied!", f"Title should be 'Copied!' after click, got {title_after}"

        # Verify text content also changed to Copied!
        text_after = address_element.inner_text()
        assert text_after == "Copied!", f"Text should be 'Copied!' after click, got {text_after}"

        # Wait for timeout (2000ms) + buffer
        page.wait_for_timeout(2500)

        # Verify title restored
        title_restored = address_element.get_attribute("title")
        assert title_restored == "Click to copy IP", f"Title should be restored to 'Click to copy IP', got {title_restored}"

        browser.close()
        print("Tests passed successfully.")

if __name__ == "__main__":
    run()
