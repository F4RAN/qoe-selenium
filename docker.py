from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                          desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
driver.get('https://www.google.com')
search_box = driver.find_element_by_name('q')
search_box.send_keys('Python Selenium')
search_box.submit()

# Do more actions as needed

driver.quit()