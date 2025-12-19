import re
from playwright.sync_api import sync_playwright
from playwright.stealth import stealth_sync

def get_stock_level(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Apply stealth techniques to avoid detection
        stealth_sync(page)

        try:
            # Navigate to the product page
            page.goto(url, timeout=60000)

            page.fill('input[name="quantity"]', '9999')

            page.click('button[type="submit"]') # This selector varies by site

            # Wait for the error message (The "Leak")
            # Example message: "Value must be less than or equal to 342."
            error_message = page.locator('.error-msg').inner_text()

            # Extract the number using Regex
            stock_number = int(re.search(r'\d+', error_message).group())
            return stock_number
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            browser.close()
