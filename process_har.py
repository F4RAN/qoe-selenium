import json
import os
import re
import urllib.request
from datetime import datetime
from time import sleep

from calculate_parameters import calculate_qos
from test import convert_ts_to_mp4, calculate_mos

downloaded_files = []
all_results = []

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)


def calculate(urls, test_model):
    converted_to_mp4 = []
    for url in urls:
        print(url)
        file_name = f"{url.split('.ts')[0].split('/')[-1]}-{datetime.timestamp(datetime.now())}"
        urllib.request.urlretrieve(url, f"./libs/ts_files/{file_name}.ts")
        convert_ts_to_mp4(file_name)
        converted_to_mp4.append(file_name)
    qos = calculate_qos()
    mos = calculate_mos(converted_to_mp4)
    test_model.set_mos(mos)
    test_model.set_qos(qos)

    # Exit Point

    print("=-=-=-=-=-=-=-=- MOS Calculation Completed =-=-=-=-=-=-=-=-=-")
    print("Score is:" + " " + str(mos))
    print("=-=-=-=-=-=- Process terminated successfully. =-=-=-=-=-=-=-")

    # DB Jobs
    test_model.create_db_record()
    test_model.insert_db_record()
    test_model.drop_db_connection()
    print("Cleaning up mp4_files directory...")
    clear_directory("./libs/mp4_files")
    print("Data Collection Success.")
    print("Go to the next process.")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


def process_har(har, test_model):
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
            pass
    print(urls)
    calculate(urls, test_model)
