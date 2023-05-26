import json
import os
import sys
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

from process_har import process_har


stopped = False

def hover(driver):
    action = ActionChains(driver)
    player = driver.find_element(By.CLASS_NAME, 'player-wrapper')
    action.move_to_element(player).perform()
    sleep(1)

def run(url):
    global stopped
    duration = 10
  
    os.popen("java -jar ./libs/browsermob-proxy-2.1.4/lib/browsermob-dist-2.1.4.jar --port 9090")
    sleep(10)
    server = Server("./libs/browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 9090})
    server.start()
    proxy = server.create_proxy()

    co = webdriver.ChromeOptions()
    co.add_argument('--ignore-ssl-errors=yes')
    co.add_argument('--ignore-certificate-errors')
    co.add_argument('--proxy-bypass-list=aparat.com"')
    # co.add_argument('--headless')
    co.add_argument('--mute-audio')
    co.add_argument("--autoplay-policy=no-user-gesture-required");
    co.add_argument('--disable-gpu')
    co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))

    driver = webdriver.Chrome(service=Service(r'./libs/chromedriver'), options=co)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=co)
    print('===============QoE Assessment in Multimedia===============')
    print(f"Request to {url}")

    proxy.new_har("aparat.ir/")
    driver.get(url)
    sleep(2)
    driver.implicitly_wait(5000)
    wait = WebDriverWait(driver, 10)
    advertise = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'vast-skip-button')))

    # advertise= driver.find_element(By.CLASS_NAME, "vast-skip-button")
    if advertise: advertise.click()
    print('video started')
    sleep(duration)

    hover(driver)

    try:
        driver.find_element(By.CLASS_NAME, "romeo-button").click()
    except:
        server.stop()
        driver.quit()
        stopped = True
    print(f'after {duration} seconds video stopped')
    # driver.close()
    print("process ended.")
    print('===============QoE Assessment in Multimedia===============')

    with open("network_log1.har", "w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))

    if not stopped:
        server.stop()
        driver.quit()

    process_har(json.dumps(proxy.har))

if __name__ == '__main__':
    if(len(sys.argv)<2 or len(sys.argv)>2):
        print("please enter a video url")
        exit(1)
    run(sys.argv[1])
