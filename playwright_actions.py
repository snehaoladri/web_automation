from playwright.sync_api import sync_playwright
import time

import undetected_chromedriver as uc
from entity_prediction import extract_entities_llama
import time
import json

HOST = "REPLACE WITH BRIGHTDATA HOST"
USERNAME = "REPLACE WITH BRIGHTDATA USRNAME"
PASSWORD = "REPLACE WITH BRIGHTDATA PASSWORD"
# driver.quit()
def navigate_bunnings(user_input, recover=False):
    entities = extract_entities_llama(user_input)
    brand = entities.get("brand", "")
    product = entities.get("product", "")
    price = entities.get("price", "")
    color = entities.get("color", "")

    if not product:
        raise ValueError("❌ LLaMA could not extract product entity from input.")

    search_query = f"{color} {brand} {product}".strip()
    search_query=user_input
    print(f"[INFO] Final search query: '{search_query}'")
    with sync_playwright() as p:
        print("[INFO] Launching Firefox browser...")
        user_data_dir = "/tmp/test-user-data-dir"
        proxies={"server":HOST,
                  "username":USERNAME,
                  "password":PASSWORD}
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=True,
            proxy=proxies,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-http2",
                "--disable-blink-features=AutomationControlled",
                "--ignore-certificate-errors",
                "--disable-features=UseChromiumNetworkService,NetworkService",
                "--disable-features=SitePerProcess,IsolateOrigins",
                "--window-size=1280,800"
            ]
        )
        print("[INFO] Launched Firefox browser...")
        page = browser.new_page()

        try:
            print(f"[INFO] Navigating to Bunnings homepage...")
            page.goto("http://www.bunnings.com.au", wait_until='load',timeout=200000)
            page.screenshot(path="bunnings.png")
            for attempt in range(3):
                try:
                    print(f"[INFO] Waiting for Search input — attempt {attempt + 1}")
                    page.wait_for_selector("#custom-css-outlined-input", timeout=90000)
                    print("[SUCCESS] Search input appeared.")
                    break
                except:
                    page.screenshot(path="bunnings_attempt.png")
                    print(f"[WARN] Not yet visible, waiting more... (attempt {attempt + 1})")
                    time.sleep(3)
            else:
                page.screenshot(path="cloudflare_timeout.png")
                raise Exception("Cloudflare did not clear — search input never appeared.")
            print("taking screenshot")
            page.screenshot(path="bunnings_debug.png")
            search_box = page.locator("#custom-css-outlined-input")
            search_trigger = page.locator("form#header-search div[role='button']")
            print("in searching")
            search_box.fill(search_query)
            # search_box.focus()
            page.screenshot(path="debug_before_search_click.png")
            print("falling back to keyboard...")
            search_box.focus()
            with page.expect_navigation(url="**/search/**",wait_until="domcontentloaded", timeout=0):
                page.keyboard.press("Enter")
            print("[DEBUG] Current URL:", page.url)
            page.screenshot(path="before_load.png")
            try:
                page.wait_for_load_state()
            except Exception as e:
                print("Looks like page is already loaded, going to next step")

            page.screenshot(path="debug_after_search_submit.png")
            print("[SUCCESS] Search triggered.")
            print("waiting for selector")
            page.wait_for_selector("article[data-locator^='search-product-tile-index-']", timeout=60000)
            print('locating product')
            first_article = page.locator("article[data-locator='search-product-tile-index-0']")
            product_link = first_article.locator("a[data-locator^='image-rating-']")

            # Ensure the link is visible and enabled
            product_link.wait_for(state="visible", timeout=5000)
            print("[INFO] Clicking on product...")
            product_link.click()
            print("[DEBUG] URL after click:", page.url)
            page.screenshot(path="bunnings_click1.png")
            # Wait for the product page to fully load
            page.wait_for_load_state("load")
            page.wait_for_selector("button:has-text(\"Add to Cart\")")
            page.screenshot(path="bunnings_click.png")
            page.click("button:has-text(\"Add to Cart\")")
            page.screenshot(path="bunnings_add.png")
            page.locator("button[data-locator='icon-cart']")
            page.click("button[data-locator='icon-cart']")
            page.screenshot(path="bunnings_cart.png")
            page.wait_for_selector("a:has-text(\"Checkout\")")
            page.click("a:has-text(\"Checkout\")")

            url = page.url
            browser.close()
            print('browser closed')
            return f"Navigation successful. Final page: {url}"

        except Exception as e:
            print('In Exception',e)
            page.screenshot(path="bunnings_exception.png")
            browser.close()
            if recover:
                return f"Recovery failed: {str(e)}"
            raise e

navigate_bunnings('white pen marker')