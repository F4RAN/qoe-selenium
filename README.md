# PLEASE CREATE FILES FIRST 

At first you must to create shared folder with 3 files:

1- aparat_file.txt, 

2- network_performance.db,

3- config.txt

### Files Description

`aparat.txt`: copy from aparat.txt in root of project ( you can access it Here and copy records to paste in your aparat.txt file)

`config.txt`: 
Set network parameters (if you dont want each limitation you can simply remove that line)
```
rate 100Kbps
delay 100ms
loss 10%
```

`network_performance.db`: after running program, results live saved into this file.

### LINUX
```
mkdir /path/to/shared/ && cd /path/to/shared/
touch aparat_file.txt && touch network_performance.db && touch config.txt
```
* Choose a custom path instead of /path/to/shared

### WINDOWS
```
mkdir C:\shared & cd C:\shared & type nul > aparat_file.txt & type nul > network_performance.db & type nul > config.txt 
```



# RUN PROJECT
## LINUX

#### AMD Arch
```
docker run -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
```
#### ARM Arch
```
docker run -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-arm
```

## WINDOWS:

```
docker run -v //c/shared/aparat_file.txt:/usr/src/app/aparat_file.txt -v //c/shared/network_performance.db:/usr/src/app/network_performance.db -v //c/shared/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
```





