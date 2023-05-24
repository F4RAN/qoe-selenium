import os
import sys
from time import sleep
from browsermobproxy import Server
from selenium import webdriver
from main import crawl



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
    # co.add_argument('--headless')
    co.add_argument('--mute-audio')
    co.add_argument('--disable-gpu')
    co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))
    driver = webdriver.Chrome(executable_path=r'./libs/chromedriver', options=co)
    proxy.new_har("aparat.ir/")
    return driver, server, proxy

def destroy(d,s,p):
    d.quit()
    s.stop()
    os.system("pkill -f 'java -jar ./libs/browsermob-proxy-2.1.4/lib/browsermob-dist-2.1.4.jar'")


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
                print("ENDED")
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
    if sys.argv and len(sys.argv) > 1:
        if sys.argv[1] != "--link" and sys.argv[1] != "--file":
            print("here")
            print("Please enter a valid format:")
            print("python3 app.py --link aparat_url_1, aparat_url_2, aparat_url_3 ...")
            print("python3 app.py --file path/to/aparat_urls")
            exit(1)
        driver, server, proxy = initialize()
        process_input(sys.argv, driver, server, proxy)
    else:
        print("Please enter a valid format:")
        print("python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3,...")
        print("python3 app.py --file path/to/aparat_urls")
        exit(1)