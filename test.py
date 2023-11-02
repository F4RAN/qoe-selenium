import os
import subprocess
from os.path import abspath
import sys
sys.path.append('./libs/itu-p1203-master')
from itu_p1203 import extractor
from itu_p1203 import p1203_standalone


def convert_ts_to_mp4(ts):
    print(f"Converting {ts} to mp4...")
    command = ['ffmpeg', '-i', f'./libs/ts_files/{ts}.ts', '-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-f', 'mp4', f'./libs/mp4_files/{ts}.mp4']
    try:
        result = subprocess.run(command, timeout=10, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("FFMEPG TIMED OUT")
        return False
    if result.returncode == 0:
        return True
    else:
        return False

def calculate_mos(mp4s,stalling):
    print(f"Calculating mos...")
    address = []
    for mp4 in mp4s:
        address.append(f'./libs/mp4_files/{mp4}.mp4')
    input_data = extractor.Extractor(address, 3)  # input .ts files, mode
    inp = input_data.extract()
    # Calculate Stalling Here
    for stall in stalling:
        inp['I23']['stalling'].append(stall)
    # Use p1203_standalone to calculate parameters and send it to output
    out = p1203_standalone.P1203Standalone(inp)
    res = out.calculate_complete()
    return res['O46']


def test_mp4_file():
    input_data = extractor.Extractor(["./test/jadi-low-again.mp4"], 3)  # input .ts files, mode
    inp = input_data.extract()
    # Use p1203_standalone to calculate parameters and send it to output
    out = p1203_standalone.P1203Standalone(inp)
    print(out.calculate_complete())

def get_ts_files():
    files = os.listdir('./libs/ts_files')
    ts_files = []
    for file in files:
        if file.find(".ts") != -1:
            ts_files.append(file)
    return sorted(ts_files, key=lambda x: int(x.split("-")[1]))  # sort by number

if __name__ == '__main__':
    # test_mp4_file()
    ts_files = get_ts_files()
    string = ""
    result = "./results/output.json"

    for (index,ts) in enumerate(ts_files):
        ts_files[index] = "./libs/ts_files/"+ ts
    # Use extractor class to create input json from video file
    input_data = extractor.Extractor(ts_files,3) # input .ts files, mode
    inp = input_data.extract()
    """
    We have to push stalling events like [stalling-start-timestamp, stalling-duration] into the inp['I23']['stalling']
    example: inp['I23']['stalling'].append([1678660882,1678662882])
    """
    # Use p1203_standalone to calculate parameters and send it to output
    out = p1203_standalone.P1203Standalone(inp)
    print(out.calculate_complete())