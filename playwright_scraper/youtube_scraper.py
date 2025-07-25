from playwright.sync_api import sync_playwright
import time

def scrape_youtube(url, personalization_type):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
            # Handle consent dialog
            time.sleep(2) # wait for dialog to appear
            consent_button = page.locator("button[aria-label*='Accept']").first
            if consent_button.is_visible():
                consent_button.click()

            about_url = f"{url.rstrip('/')}/about"
            page.goto(about_url, timeout=60000)
            page.wait_for_selector("yt-formatted-string.style-scope.ytd-channel-name", timeout=60000)

            channel_name = page.locator("yt-formatted-string.style-scope.ytd-channel-name").first.inner_text()
            about = page.locator("yt-formatted-string#description").first.inner_text()

            if personalization_type == "Overall Channel-Based":
                return {
                    "channel_name": channel_name,
                    "about": about
                }
            
            elif personalization_type == "Latest Video-Based":
                videos_url = f"{url.rstrip('/')}/videos"
                page.goto(videos_url, timeout=60000)
                
                # Click the "Videos" tab
                page.locator("div.yt-tab-shape-wiz__tab:has-text('Videos')").click()
                
                page.wait_for_selector("ytd-rich-grid-media", timeout=60000)
                
                latest_video = page.locator("ytd-rich-grid-media").first
                latest_video_title = latest_video.locator("#video-title").inner_text()
                latest_video_url = latest_video.locator("a#video-title-link").get_attribute('href')

                page.goto(f"https://www.youtube.com{latest_video_url}", timeout=60000)
                page.wait_for_selector("#description-inline-expander", timeout=60000)
                video_description = page.locator("#description-inline-expander").first.inner_text()

                return {
                    "channel_name": channel_name,
                    "about": about,
                    "latest_video_title": latest_video_title,
                    "video_description": video_description
                }

        except Exception as e:
            print(f"Error scraping YouTube: {e}")
            return None
        finally:
            browser.close()
