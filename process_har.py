import json
import re

har_file_path = "network_log1.har"
with open(har_file_path, "r", encoding="utf-8") as f:
    logs = json.loads(f.read())

# Store the network logs from 'entries' key and
# iterate them
network_logs = logs['log']['entries']
for log in network_logs:
    try:
        # URL is present inside the following keys
        url = log['request']['url']
        is_ts = re.search('.*\.ts',url)
        """
        Every .ts file contains 10 seconds of aparat video; 
        we want to pass these files to the ITU-T P1203 Input.
        """
        if(is_ts): print(url)
    except Exception as e:
        pass