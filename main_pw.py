from playwright.sync_api import sync_playwright
import time
playwright = sync_playwright().start()
# Use playwright.chromium, playwright.firefox or playwright.webkit
# Pass headless=False to launch() to see the browser UI
browser = playwright.chromium.launch(headless=False)
browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.4692.71 Safari/537.36")
page = browser.new_page()
url = "https://www.aparat.com/v/DZ93y"
print(f"Request to {url}")
page.goto(url)
# controls = driver.find_element(By.CLASS_NAME, "romeo-controls")
c = 0
while True:
    try:
        controls = page.query_selector(".romeo-controls")
        classess = controls.get_attribute("class").split()
        if controls and ("ad-mode" not in classess):
            break
        elif controls and ("ad-mode" in classess):
            print("Finding skip button, Please wait...")
            try:
                skip = page.query_selector('.vast-skip-button')
                skip.click()
            except:

                try:
                    play = page.query_selector('.romeo-play-toggle')
                    print("here")
                    if play: label = play.get_attribute("aria-label")
                    if play and label == "پخش K":
                        play.click()
                except:
                    print("here")
                    pass
                # $('.romeo-play-toggle').getAttribute('aria-label') == "پخش K"

                pass
    except:
        print(f"{c} - problem with advertisement wait for timeout")
        pass
    page.screenshot(path=f"tst.png")
    time.sleep(0.5)
    c += 1

browser.close()
playwright.stop()