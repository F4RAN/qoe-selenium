## Installation scenario on Ubuntu
first you should install git, python3 and ffmpeg:
```
sudo apt install git python3 ffmpeg
```
then install the required packages using the command below:
```
sudo apt-get install libavformat-dev libavdevice-dev libavfilter-dev libswscale-dev
```
To export ffmpeg_debug_qp to your PATH first you need to clone the following project:
```
git clone https://github.com/slhck/ffmpeg-debug-qp.git
```
Then navigate to the cloned directory:
```
cd ffmpeg-debug-qp
```
build the tool:
```
make
```
After building, you need to add the tool to your system's PATH.you can move the ffmpeg_debug_qp executable to /usr/local/bin:
```
sudo mv ffmpeg_debug_qp /usr/local/bin
```
Now, ffmpeg_debug_qp should be available system-wide. You can verify this by typing ffmpeg_debug_qp in your terminal. If it's correctly installed, you should see the usage instructions for the tool.
Please note that you need to have make installed on your system to build ffmpeg_debug_qp.

then you should install qoe-selenium project:
```
git clone https://github.com/F4RAN/qoe-selenium.git && cd qoe-selenium && pip3 install -r requirements.txt
```



## Run App
Run comma separated links:
```bash
# Command
python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3 ...

# Example
python3 app.py --link https://www.aparat.com/v/BQSoN,https://www.aparat.com/v/eBvdL,https://www.aparat.com/v/2AtcF
```
Run file (each line including one link)
```bash
# Command
python3 app.py --file path/to/aparat_urls

# Example
python3 app.py --file ./aparat_file.txt
```
file structure: aparat_file.txt:


![img.png](img.png)

You must use compatible chromedriver of your os, you can use below link to download suitable version of chrome depended on your Chrome version:
https://chromedriver.chromium.org/downloads


## Installation scenario on macOS
this implementation just works on ffmpeg version 4

    brew install ffmpeg@4 pkg-config

after communication with main developer of [ffmpeg-debug-qp](https://github.com/slhck/ffmpeg-debug-qp/issues/38),
i found out i must use this command after clone `ffmpeg-debug-qp` package 


    export PKG_CONFIG_PATH="/opt/homebrew/opt/ffmpeg@4/lib/pkgconfig
and use `make` command to compile it root folder of `ffmpeg-debug-qp`

then copy builded file to the with below command:
    
    sudo cp ./ffmpeg_debug_qp /usr/local/bin/

so now [itu_p1203](https://github.com/itu-p1203/itu-p1203) standalone app can use the `ffmpeg_debug_qp` correctly.


## Database fields
`test_no`: number of test INTEGER,

`url`: url of video that we was testing it TEXT,

`timestamp`: date and time of testing DATETIME,

`delay`: from selenium in ms INTEGER,

`throughput`: from selenium in bps INTEGER,

`connection_time`: from selenium in ms INTEGER,

`ttfb`: time to first byte from selenium in ms INTEGER,

`content_load_time`: from selenium in ms INTEGER,

`mos`: *100 in INTEGER,

`initial_load_time`: from selenium in ms INTEGER,

`page_load_time`: from code ms INTEGER,

`css_load_time`: from selenium in ms INTEGER,

`js_load_time`: from selenium in ms INTEGER,

`video_load_time`: from selenium in ms INTEGER,

`html_load_time`: from selenium in ms INTEGER,

`video_width`: from selenium INTEGER,

`video_height`: from selenium INTEGER,

`main_video_duration`: video duration without advertise from selenium in ms INTEGER, 

`avg_frame_rate`: *100 from selenium INTEGER,

`startup_time`: from HAR in ms INTEGER,

`buffering_time`: from HAR in ms INTEGER,

`buffering_ratio`: from HAR in percent INTEGER,

`avg_buffering_time`: from HAR in ms INTEGER,

`total_size_with_buffer`: from HAR in bits INTEGER,

`avg_bitrate`: from HAR in kbps INTEGER,

`delay_qos`: from PING in ms INTEGER,

`jitter`: from PING in ms INTEGER,

`packet_loss`: from PING in ms INTEGER,

## Code changes
change `valid_video_exts` in `__main__.py`

    valid_video_exts = ["avi", "mp4", "mkv", "nut", "mpeg", "mpg"]

to

    valid_video_exts = ["avi", "mp4", "mkv", "nut", "mpeg", "mpg", "ts"]

<hr>

in `extractor.py` in `get_stream_size()` function change
    
    size = sum([l for l in stdout.split("\n") if l != ""])

to
    
    size = 0
    for l in stdout.split("\n"):
        if l != "":
            if l.find("|"):
                l = l.split("|")[0]
                size += int(l)
