from playwright.sync_api import sync_playwright, Page, TimeoutError

class Browser:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def navigate(self, url):
        try:
            self.page.goto(url, timeout=60000)
            return f"Navigated to {url}"
        except TimeoutError:
            return f"Timeout error while navigating to {url}"

    def scroll_down(self, times=1):
        for _ in range(times):
            self.page.evaluate("window.scrollBy(0, window.innerHeight)")
        return f"Scrolled down {times} times"

    def click(self, selector):
        try:
            self.page.click(selector, timeout=10000)
            return f"Clicked on element with selector '{selector}'"
        except TimeoutError:
            return f"Timeout error while clicking on selector {selector}"

    def extract_html(self, selector=None):
        if selector:
            return self.page.inner_html(selector)
        return self.page.content()

    def get_visible_texts(self):
        return self.page.locator('body').inner_text()

    def close(self):
        self.browser.close()
        self.playwright.stop()
