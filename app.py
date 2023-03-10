import json
import os
import subprocess
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = "https://www.aparat.com/faarawn"
duration = 10


def hover(driver):
    action = ActionChains(driver)
    player = driver.find_element(By.CLASS_NAME, 'player-wrapper')
    action.move_to_element(player).perform()
    sleep(1)


os.popen("java -jar ./libs/browsermob-proxy-2.1.4/lib/browsermob-dist-2.1.4.jar --port 9090")
sleep(10)
server = Server("./libs/browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 9090})
server.start()
proxy = server.create_proxy()

co = webdriver.ChromeOptions()
co.add_argument('--ignore-ssl-errors=yes')
co.add_argument('--ignore-certificate-errors')
co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))

driver = webdriver.Chrome(executable_path=r'./libs/chromedriver', options=co)
print('===============QoE Assessment in Multimedia===============')
print(f"Request to {url}")

proxy.new_har("aparat.ir/")
driver.get(url)
sleep(2)
elem = driver.find_element(By.CLASS_NAME, "poster")
elem.click()
driver.implicitly_wait(5000)
control_button = driver.find_element(By.CLASS_NAME, "romeo-player-tooltip")

wait = WebDriverWait(driver, 10)
advertise = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'vast-skip-button')))

# advertise= driver.find_element(By.CLASS_NAME, "vast-skip-button")
if advertise: advertise.click()
print('video started')
sleep(duration)

hover(driver)

driver.find_element(By.CLASS_NAME, "romeo-button").click()
print(f'after {duration} seconds video stopped')
# driver.close()
print("process ended.")
print('===============QoE Assessment in Multimedia===============')

with open("network_log1.har", "w", encoding="utf-8") as f:
    f.write(json.dumps(proxy.har))

server.stop()
driver.quit()
