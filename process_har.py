import json
import os
import re
import urllib.request
from datetime import datetime
from time import sleep

from calculate_parameters import calculate_qos
from calculate_stalling import calculate_stalling
from test import convert_ts_to_mp4, calculate_mos

downloaded_files = []
all_results = []




def calculate(urls, test_model, stalling):
    print("1")
    converted_to_mp4 = []
    file_names = []
    for url in urls:
        # quality = url.split(".apt")[0].split("/")[4].split("-")[1]
        file_name = f"{url.split('.ts')[0].split('/')[-1]}"
        if file_name in file_names:
            continue
        print(url)
        file_names.append(file_name)
        urllib.request.urlretrieve(url, f"./libs/ts_files/{file_name}.ts")
        convert_ts_to_mp4(file_name)
        converted_to_mp4.append(file_name)
    print("2")
    try:
        qos = calculate_qos()
        test_model.set_qos(qos)
    except Exception as e:
        print(e)

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


def process_har(har, test_model, stalling):
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
