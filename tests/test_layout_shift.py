from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        html_file = os.path.abspath(os.path.join("/app", "index.html"))
        page.goto(f"file://{html_file}")

        server_addr = page.locator(".server-address")
        server_addr.wait_for(state="attached")

        box_before = server_addr.bounding_box()
        print(f"Box before: {box_before}")

        server_addr.click()
        page.wait_for_timeout(100)

        box_after = server_addr.bounding_box()
        print(f"Box after: {box_after}")

        if box_before['width'] != box_after['width']:
            print("Layout shift detected!")
            print(f"Width changed from {box_before['width']} to {box_after['width']}")
        else:
            print("No layout shift.")

        browser.close()

if __name__ == "__main__":
    run()
