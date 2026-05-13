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

        test_html_file = os.path.abspath(os.path.join("/app", "tests", "test_iframe.html"))
        if not os.path.exists(os.path.dirname(test_html_file)):
             test_html_file = os.path.abspath(os.path.join(os.getcwd(), "tests", "test_iframe.html"))

        # Create a test HTML file that embeds index.html in a restrictive sandbox
        with open(test_html_file, 'w') as f:
            f.write(f'''
            <!DOCTYPE html>
            <html>
            <head><title>Test Iframe</title></head>
            <body>
                <iframe src="file://{html_file}" sandbox="allow-scripts" id="test-iframe"></iframe>
            </body>
            </html>
            ''')

        errors = []
        page.on("pageerror", lambda err: errors.append(err.message))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" and "Frame-busting blocked" not in msg.text and "SecurityError" in msg.text else None)

        try:
            # Navigate to the test HTML file
            page.goto(f"file://{test_html_file}")

            # Wait a bit for the iframe to load and execute its script
            page.wait_for_timeout(1000)

            # We check the iframe's content directly. Because of strict origin policies
            # and sandboxing with file:// URLs, accessing frame content might be blocked,
            # but our main goal is to ensure NO unhandled page errors bubble up.

            # Since the inner frame threw a DOMException before, we check if our pageerror
            # listener caught any unhandled exception.

            has_dom_exception = any("DOMException" in str(err) or "SecurityError" in str(err) for err in errors)

            assert not has_dom_exception, f"Found unhandled DOMException or SecurityError leaking: {errors}"
            print("Test passed: Frame-busting logic gracefully handles sandboxed environments without leaking unhandled exceptions.")

        finally:
            browser.close()
            # Clean up the test HTML file
            if os.path.exists(test_html_file):
                os.remove(test_html_file)

if __name__ == "__main__":
    run()
