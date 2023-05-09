import json
import re
import urllib.request
from datetime import datetime
from haralyzer import HarParser, HarPage

import db
from test import convert_ts_to_mp4, calculate_mos

# har_file_path = "network_log1.har"
# with open(har_file_path, "r", encoding="utf-8") as f:
#     logs = json.loads(f.read())

# Store the network logs from 'entries' key and
# iterate them
# network_logs = logs['log']['entries']

downloaded_files = []

all_results = []


def calculate(urls, test_model):
    converted_to_mp4 = []
    for url in urls:
        print(url)
        file_name = f"{url.split('.ts')[0].split('/')[-1]}-{datetime.timestamp(datetime.now())}"
        urllib.request.urlretrieve(url, f"./libs/ts_files/{file_name}.ts")
        convert_ts_to_mp4(file_name)
        converted_to_mp4.append(file_name)

    mos = calculate_mos(converted_to_mp4)
    test_model.set_mos(mos)
    print("=-=-=-=-=-=-=-=- MOS Calculation Completed =-=-=-=-=-=-=-=-=-")
    print("Score is:" + " " + str(mos))
    print("=-=-=-=-=-=- Process terminated successfully. =-=-=-=-=-=-=-")

    # DB Jobs
    test_model.create_db_record()
    test_model.insert_db_record()
    test_model.drop_db_connection()
    print("Data Collection Success.")


def process_har(har, test_model):
    urls = []
    test_model.extract_har_parameters(har)
    for log in json.loads(har)['log']['entries']:
        try:
            # URL is present inside the following keys
            url = log['request']['url']
            is_ts = re.search('.*\.ts', url)
            is_ad = re.search('ad', url)
            """
            Every .ts file contains 10 seconds of aparat video; 
            we want to pass these files to the ITU-T P1203 Input.
            """

            if is_ts and not is_ad: urls.append(url)
        except Exception as e:
            pass
    calculate(urls, test_model)


