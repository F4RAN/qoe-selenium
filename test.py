import os
import subprocess
from os.path import abspath
import sys
import requests
import urllib.request
sys.path.append('./libs/itu-p1203-master')
from itu_p1203 import extractor
from itu_p1203 import p1203_standalone

file_name = "down_vid"
file_name=file_name+".mp4"
file_dir=os.path.abspath('./tmp/')  
work_path=os.path.join(file_dir,file_name) 

ts_files_path="./libs/my_ts_files"

def get_ts_files():
    files = os.listdir(ts_files_path)
    ts_files = []
    for file in files:
        if file.find(".ts") != -1:
            ts_files.append(file)
    return sorted(ts_files, key=lambda x: int(x.split("-")[1]))  # sort by number

def download_video(url):
    try:
        print("Downloading starts...\n")
        urllib.request.urlretrieve(url, work_path)
        print("Download completed..!!")
    except Exception as e:
        print(e)

def split_mp4_to_ts_files():
    split_command="ffmpeg -re -i " + work_path +" \
        -codec copy -map 0 \
        -f segment -segment_list playlist.m3u8 \
        -segment_list_flags +live -segment_time 10 \
        "+ts_files_path+"/s-%d-v1-a1.ts"
    os.system(split_command)
    
    
    
if __name__ == '__main__':
    os.system("rm -f "+work_path)
    os.system("rm -rf "+ts_files_path+";mkdir "+ts_files_path)
    
    url=input("get url : ") #https://www.aparat.com/v/hBp7D
    hash_url=(url.split("/"))[-1]
    response = requests.get("https://www.aparat.com/etc/api/video/videohash/"+hash_url)
    file_link=response.json()["video"]["file_link"]


    download_video(file_link)
    split_mp4_to_ts_files()
    ts_files = get_ts_files()
    string = ""
    result = "./results/output.json"
    p1202_src = "./libs/itu-p1203-master/itu_p1203"
    for (index,ts) in enumerate(ts_files):
        ts_files[index] = ts_files_path+"/"+ ts
    # Use extractor class to create input json from video file
    input_data = extractor.Extractor(ts_files,3) # input .ts files, mode
    inp = input_data.extract()
    # Use p1203_standalone to calculate parameters and send it to output
    out = p1203_standalone.P1203Standalone(inp)
    print(out.calculate_complete())