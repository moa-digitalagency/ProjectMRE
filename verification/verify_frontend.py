from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            print("Navigating to http://127.0.0.1:5000")
            page.goto("http://127.0.0.1:5000", timeout=60000)
            page.wait_for_load_state("networkidle")

            # Verify title
            title = page.title()
            print(f"Page title: {title}")
            assert "Village Seniors" in title

            # Verify slider exists
            slider = page.locator("#slider")
            if slider.count() > 0:
                print("Slider found.")
            else:
                print("Slider NOT found.")

            # Take screenshot
            screenshot_path = "verification/verification.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
