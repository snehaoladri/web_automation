from playwright.sync_api import sync_playwright
import time

import undetected_chromedriver as uc
import time
import json

# options = uc.ChromeOptions()
# options.add_argument("--headless=new")  # Use headless=new to minimize detection
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-blink-features=AutomationControlled")

# driver = uc.Chrome(options=options)

# driver.get("https://www.bunnings.com.au")
# time.sleep(30)  # Wait manually for Cloudflare to complete if needed

# # Optional: print cookies to reuse later in Playwright
# cookies = driver.get_cookies()
# with open("cf_cookies.json", "w") as f:
#     json.dump(cookies, f, indent=2)

# driver.quit()
def navigate_bunnings(product_name, recover=False):
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        # browser = await playwright.chromium.launch(headless=False)
        print("[INFO] Launching Firefox browser...")
        user_data_dir = "/tmp/test-user-data-dir"
        proxies={"server":"brd.superproxy.io",
                  "username":"brd-customer-hl_59b47a88-zone-web_unlocker1",
                  "password":"6600142i4fo8"}
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
                "--proxy-server='direct://'",
                "--proxy-bypass-list=*",
                "--window-size=1280,800"
            ]
        )
        print("[INFO] Launched Firefox browser...")
        # with open("cf_cookies.json") as f:
        #     cookies = json.load(f)
        

        cf_cookies = [
            {
                "name": "cf_clearance",
                "value": "IyNTUtJ8magZoP4YxUNMuFJRDNMi912PfdnOspymcug-1750237078-1.2.1.1-NcfmaX7skKo7aIHuSsX8fbZlLO4bwR7vATjLbRSAR1FJBplZeUpQZWpPCjzD7bXK9ozUqiRLkam4Oqx5CLze1jU82R3DPWh94dmgKtMx..6yh4L2YvHFX0yQdyEdV5lWBYsMkn8UHBebZMGSwKxOe3ig9tANVdZ5ip31YoeAp_bbs3zOq1zvIqJCkIJHZBvXh_YMvwqudo3jgvdyU0J4H26Kj1EzWb7JD9rwJlbn6C2CaLQbhLsK7DmkizAKGQzvA0rC4cH8i0rDaSkaipDaaXVv1bKmqJP5ZPgTKlNO8W84SRGD_ZP7IjTSDz6s2vGKOSiORmCZgtl3ksddfkJRrmALJSbXijAoz4_t4uR3Cla4J.W_L8Z_BwrQnnoP766U",
                "domain": ".bunnings.com.au",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }
        ]

        # browser.add_cookies(cf_cookies)
        page = browser.new_page()
        # page = browser.new_page()

        try:
            # page.on("console", lambda msg: print(f"[Console] {msg.type}: {msg.text}"))
            print(f"[INFO] Navigating to Bunnings homepage...")
            page.goto("http://www.bunnings.com.au", wait_until='load',timeout=200000)
            page.screenshot(path="bunnings.png")
            # page.wait_for_function(
            #     """() => document.querySelector("input[placeholder='Search']") !== null""",timeout=200000
            # )
            for attempt in range(3):
                try:
                    print(f"[INFO] Waiting for Search input — attempt {attempt + 1}")
                    page.wait_for_selector("input[placeholder='Search']", timeout=60000)
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
            search_box = page.locator("input[placeholder='Search']")
            print("in searching")
            search_box.fill(product_name)
            # page.get_by_placeholder("Search").fill(product_name)
            print("pressing enter")
            page.keyboard.press("Enter")
            print("waiting for selector")
            page.wait_for_selector(".product-title")

            page.click(".product-title a")
            page.wait_for_selector("button:has-text(\"Add to Cart\")")
            page.click("button:has-text(\"Add to Cart\")")

            page.click("a:has-text(\"Cart\")")
            page.wait_for_selector("a:has-text(\"Checkout\")")
            page.click("a:has-text(\"Checkout\")")

            url = page.url
            browser.close()
            print('browser closed')
            return f"Navigation successful. Final page: {url}"

        except Exception as e:
            page.screenshot(path="bunnings_exception.png")
            print('Exception',e)
            browser.close()
            if recover:
                return f"Recovery failed: {str(e)}"
            raise e
