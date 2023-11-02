import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.exceptions import Timeout
from calculate_parameters import calculate_qos
from test import convert_ts_to_mp4, calculate_mos

downloaded_files = []
all_results = []
def delete_config():
    global config_found
    if config_found:
        os.system("tcdel eth0 --all")
    config_found = False
    return


def calculate(urls, test_model, stalling):
    print("1")
    try:
        qos = calculate_qos()
        test_model.set_qos(qos)
    except Exception as e:
        print(e)

    delete_config()

    print("2")

    def download_and_convert(url):
        file_name = f"{url.split('.ts')[0].split('/')[-1]}"
        if file_name in file_names:
            return
        try:
            response = requests.get(url, timeout=10)
            with open(f'./libs/ts_files/{file_name}.ts', 'wb') as f:
                f.write(response.content)
        except Timeout:
            print(f"Timeout occurred downloading {url}")
            return
        # urllib.request.urlretrieve(url, f"./libs/ts_files/{file_name}.ts")


        res = convert_ts_to_mp4(file_name)
        if not res:
            return
        return file_name

    converted_to_mp4 = []
    file_names = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(download_and_convert, urls)
        for file_name in results:
            if file_name:
                converted_to_mp4.append(file_name)
                file_names.append(file_name)


    # for url in urls:
    #     # quality = url.split(".apt")[0].split("/")[4].split("-")[1]
    #     file_name = f"{url.split('.ts')[0].split('/')[-1]}"
    #     if file_name in file_names:
    #         continue
    #     print(url)
    #     file_names.append(file_name)
    #     urllib.request.timeout = 240
    #     urllib.request.urlretrieve(url, f"./libs/ts_files/{file_name}.ts")
    #     convert_ts_to_mp4(file_name)
    #     converted_to_mp4.append(file_name)



    print("3")
    # stalling = []
    try:
    #     stalling = calculate_stalling(converted_to_mp4)
    #     # stalling = [[0,0], [10.13, 2.206], [32.486, 3.99]] # TEST
        test_model.set_stalling(stalling)
    except Exception as e:
        print(e)

    print("4")
    try:
        mos = calculate_mos(converted_to_mp4, stalling)
        test_model.set_mos(mos)
    except Exception as e:
        print(e)
        return False
    
    
    

    # Exit Point

    print("=-=-=-=-=-=-=-=- MOS Calculation Completed =-=-=-=-=-=-=-=-=-")
    print("Score is:" + " " + str(mos))
    print("=-=-=-=-=-=- Process terminated successfully. =-=-=-=-=-=-=-")

    # DB Jobs
    test_model.create_db_record()
    test_model.insert_db_record()
    test_model.drop_db_connection()

    print("Data Collection Success.")
    print("Go to the next process.")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

config_found = False
def process_har(har, test_model, stalling, cf):
    global config_found
    config_found = cf
    urls = []
    test_model.extract_har_parameters(har)
    for log in json.loads(har)['log']['entries']:
        try:
            # URL is present inside the following keys
            url = log['request']['url']

            is_ts = re.search(r'.*/aparat-video/.*\.ts', url)
            """
            Every .ts file contains 10 seconds of aparat video; 
            we want to pass these files to the ITU-T P1203 Input.
            """

            if is_ts: urls.append(url)
        except Exception as e:
            print(e)
            pass
    calculate(urls, test_model, stalling)
