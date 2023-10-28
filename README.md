# PLEASE CREATE FILES AT FIRST 

At first you must to create a shared folder with 3 necessary files:

1- aparat_file.txt, 

2- network_performance.db,

3- config.txt

### Files Description

1- `aparat.txt`: copy from [aparat.txt in root of project](https://github.com/F4RAN/qoe-selenium/blob/main/aparat_file.txt) ( you can access it [Here](https://github.com/F4RAN/qoe-selenium/blob/main/aparat_file.txt) and copy records to paste in your aparat.txt file)

2- `config.txt`: 
Set network parameters (if you dont want each limitation you can simply remove that line)
```
rate 100Kbps
delay 100ms
loss 10%
```

3- `network_performance.db`: after running program, results live saved into this file.

<hr>


### LINUX ( CREATE FILES IN SINGLE COMMAND )
```
mkdir /path/to/shared/ && cd /path/to/shared/
touch aparat_file.txt && touch network_performance.db && touch config.txt
```
* Choose a custom path instead of `/path/to/shared`

### WINDOWS ( CREATE FILES IN SINGLE COMMAND )
```
mkdir C:\shared & cd C:\shared & type nul > aparat_file.txt & type nul > network_performance.db & type nul > config.txt 
```

<hr>

# LINUX RUN PROJECT

#### AMD Arch
```
docker run -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
```
#### ARM Arch
```
docker run -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-arm
```

# WINDOWS RUN PROJECT

```
docker run -v //c/shared/aparat_file.txt:/usr/src/app/aparat_file.txt -v //c/shared/network_performance.db:/usr/src/app/network_performance.db -v //c/shared/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
```


<hr>

Notice that you dont need clone project when u are using Docker

For more information of install project directly click on [Full Documentation](https://github.com/F4RAN/qoe-selenium/blob/main/DOCUMENTATION.md)




