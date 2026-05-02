from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Determine the absolute path to index.html using the /app directory
        # which is standard for tests as per memory
        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        if not os.path.exists(html_file):
            # Fallback if not run inside the expected /app environment
            html_file = os.path.abspath(os.path.join(os.getcwd(), "index.html"))

        page.goto(f"file://{html_file}")

        # Wait for the skip link
        skip_link = page.locator(".skip-to-content")
        skip_link.wait_for(state="attached")

        # Verify initial state (should have negative top value to be off-screen)
        top_before = skip_link.evaluate("el => window.getComputedStyle(el).getPropertyValue('top')")
        assert top_before.startswith("-"), f"Skip link should have a negative top value, got {top_before}"

        # Wait a bit for the page to fully load and animations to finish
        page.wait_for_timeout(500)

        # Focus the link using evaluate instead of keyboard (since the first element might not be the skip link due to browser default focus)
        skip_link.evaluate("el => el.focus()")

        # Wait for the transition to complete
        page.wait_for_timeout(300)

        # Verify focused state (top should be 0px)
        top_after = skip_link.evaluate("el => window.getComputedStyle(el).getPropertyValue('top')")
        assert top_after == "0px", f"Skip link should be at top: 0px when focused, got {top_after}"

        # Click the link to follow it
        skip_link.click()

        # Verify the main content received focus
        focused_element_id = page.evaluate("document.activeElement.id")
        assert focused_element_id == "main-content", f"Main content should be focused, but {focused_element_id} is focused"

        # Verify scroll-margin-top is set
        main_content = page.locator("#main-content")
        scroll_margin = main_content.evaluate("el => window.getComputedStyle(el).getPropertyValue('scroll-margin-top')")
        assert scroll_margin != "0px", "scroll-margin-top should be set to prevent hiding under header"

        browser.close()
        print("Tests passed successfully.")

if __name__ == "__main__":
    run()
