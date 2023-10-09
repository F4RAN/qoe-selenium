import os
import sys
import psutil
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from main import crawl

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)

def stop_proxy():
    for proc in psutil.process_iter():
        try:
            if "java" in proc.name().lower() and any("browsermob" in cmd.lower() for cmd in proc.cmdline()):
                proc.terminate()
                proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass

def initialize():
    os.popen("java -jar ./libs/browsermob-proxy-2.1.4/lib/browsermob-dist-2.1.4.jar --port 9090")
    sleep(10)
    server = Server("./libs/browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 9090})
    server.start()
    proxy = server.create_proxy()
    co = webdriver.ChromeOptions()
    co.add_argument('--ignore-ssl-errors=yes')
    co.add_argument('--ignore-certificate-errors')
    co.add_argument('--proxy-bypass-list=aparat.com"')
    co.add_argument('--headless')
    co.add_argument('--no-sandbox')
    co.add_argument('--mute-audio')
    # co.add_argument('--disable-gpu')
    co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))
    # co.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=co)
    # service = Service(executable_path='./libs/chromedriver')
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service,options=co)
    driver.set_window_size(1920, 1080)
    # driver = webdriver.Chrome(options=co)
    # driver = webdriver.Remote(
    #     command_executor='http://localhost:4444/wd/hub',
    #     options=co
    # )
    proxy.new_har("aparat.ir/")
    return driver, server, proxy


def destroy(d, s, p):
    print("Cleaning up mp4_files directory...")
    clear_directory("./libs/mp4_files")
    clear_directory("./libs/ts_files")
    d.quit()
    s.stop()
    os.popen("lsof -i :9090 | awk 'NR==2 {print $2}' | xargs kill")
    stop_proxy()


def process_input(args, d, s, p):
    result = 0
    total = 0
    if "--link" in args[1]:
        input_urls = args[2].split(",")
        total = len(input_urls)
        for i in input_urls:
            if "https://www.aparat.com/" in i:
                cleaned_url = i.replace(" ", "").replace("\n", "").strip()
                res = crawl(cleaned_url, d, s, p)
                destroy(d, s, p)
                if i != input_urls[len(input_urls)-1]:
                    d, s, p = initialize()
                if res: result += 1
            else:
                continue
    elif "--file" in args[1]:
        try:
            with open(args[2], 'r') as file:
                content = file.read()
            links = content.split("\n")
            total = len(links)
            for i in links:
                if "https://www.aparat.com/" in i:
                    cleaned_url = i.replace(" ", "").replace("\n", "").strip()
                    res = crawl(cleaned_url, d, s, p)
                    destroy(d, s, p)
                    if i != links[len(links) - 1]:
                        d, s, p = initialize()
                    if res: result += 1
                else:
                    continue
        except:
            print("file not found")
            print("Please enter a valid format:")
            print("python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3,...")
            print("python3 app.py --file path/to/aparat_urls")
            exit(1)
    print("Process Completed Successfully.")
    print(f"Result Percentage:{result}/{total}")


if __name__ == "__main__":
    try:
        os.system("pkill -f 'java -jar ./libs/browsermob-proxy-2.1.4/lib/browsermob-dist-2.1.4.jar'")
        clear_directory("./libs/mp4_files")
        clear_directory("./libs/ts_files")
    except:
        pass
    if sys.argv and len(sys.argv) > 1:
        if sys.argv[1] != "--link" and sys.argv[1] != "--file":
            print("here")
            print("Please enter a valid format:")
            print("python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3 ...")
            print("python3 app.py --file path/to/aparat_urls")
            exit(1)
        driver, server, proxy = initialize()
        process_input(sys.argv, driver, server, proxy)
    else:
        print("Please enter a valid format:")
        print("python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3,...")
        print("python3 app.py --file path/to/aparat_urls")
        exit(1)
