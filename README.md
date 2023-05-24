## Run App
Run comma separated links:
```python
# Command
python3 app.py --link aparat_url_1,aparat_url_2,aparat_url_3 ...

# Example
python3 app.py --link https://www.aparat.com/v/BQSoN,https://www.aparat.com/v/eBvdL,https://www.aparat.com/v/2AtcF
```
Run file (each line including one link)
```python
# Command
python3 app.py --file path/to/aparat_urls

# Example
python3 app.py --file ./aparat_file.txt
```

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
