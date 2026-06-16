import sys
import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch()
    # Configure context with a mobile viewport to make the toggle visible
    context = await browser.new_context(viewport={'width': 375, 'height': 667})
    page = await context.new_page()

    # Disable JS to test the static HTML state
    await page.route('**/*', lambda route: route.abort() if route.request.resource_type == 'script' else route.continue_())

    pages = ['index.html', 'how-to-join.html', 'socials.html', 'why-donate.html', 'wiki.html']
    all_passed = True

    for p in pages:
        await page.goto(f'http://localhost:8000/{p}')

        # Test toggle attributes
        toggle = page.locator('.menu-toggle')
        expanded = await toggle.get_attribute('aria-expanded')
        controls = await toggle.get_attribute('aria-controls')

        # Test nav list id
        nav = page.locator('.nav-links')
        nav_id = await nav.get_attribute('id')

        if expanded != 'false' or controls != 'main-nav' or nav_id != 'main-nav':
            print(f"FAILED on {p}: expected aria-expanded='false', aria-controls='main-nav', id='main-nav'")
            print(f"Got: aria-expanded={expanded}, aria-controls={controls}, nav id={nav_id}")
            all_passed = False
        else:
            print(f"Passed on {p}")

    await browser.close()
    if not all_passed:
        sys.exit(1)

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
