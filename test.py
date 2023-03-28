import os
import subprocess
from os.path import abspath
import sys
sys.path.append('./libs/itu-p1203-master')
from itu_p1203 import extractor
from itu_p1203 import p1203_standalone


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