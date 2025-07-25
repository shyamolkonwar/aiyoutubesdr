
from playwright.sync_api import sync_playwright

def scrape_linkedin(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url)
            page.wait_for_selector('h1')

            name = page.locator('h1').first.inner_text()
            title = page.locator('.text-body-medium.break-words').first.inner_text()
            # This is a placeholder for a more robust scraping logic
            about = page.locator('div.display-flex.ph5.pv3 > div > div > div > span').first.inner_text()

            return {
                "name": name,
                "title": title,
                "about": about
            }
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            return None
        finally:
            browser.close()
