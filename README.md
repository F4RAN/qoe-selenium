# Cite this paper if you've used this repo
`Panahi, P. H. S., Jalilvand, A. H., & Diyanat, A. (2025). An efficient network-based QoE assessment framework for multimedia networks using a machine learning approach. IEEE Open Journal of the Communications Society.`

# PLEASE CREATE FILES AT FIRST 

At first you must to create a shared folder with 3 necessary files:

1- aparat_file.txt, 

2- network_performance.db,

3- config.txt

### Files Description

1- `aparat.txt`: copy from [aparat.txt in root of project](https://github.com/F4RAN/qoe-selenium/blob/main/aparat_file.txt) ( you can access it [Here](https://github.com/F4RAN/qoe-selenium/blob/main/aparat_file.txt) and copy records to paste in your aparat.txt file)

2- `config.txt` (just create and leave it empty if you are using Windows): 
Set network parameters (if you dont want each limitation you can simply remove that line)

You can also copy the prepared configs and just paste them in your `config.txt` file. ([ to show prepared configs Click Here ](https://github.com/F4RAN/qoe-selenium/blob/main/NETWORKS.md))

For example, bottom config is related to the "Good 3G Network" to See more [Click Here](https://github.com/F4RAN/qoe-selenium/blob/main/NETWORKS.md)
```
-incoming
delay 30ms
delay-distro 7ms
loss 0%
rate 1Mbps
-outgoing
delay 30ms
delay-distro 7ms
loss 0%
rate 500Kbps
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


# SERVER 
#### Create Files
```
mkdir medium-3g && cd medium-3g && touch aparat_file.txt && touch network_performance.db && touch config.txt
```
then like other scenarios set them

#### Run detached
```
docker run -d --name medium-3g -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
```

#### Attach then
```
docker attach medium-3g
```
you can quit with `Cntrl-p` `Cntrl-q`  not `Cntrl-c`


#### Monitor databases
```
cd ~ & nano monitor.sh
```
then copy this code in it:
```
cd ~
folder="folder1 folder2 folder3"
for f in $folder; do
  echo "**********************************************************"
  echo $f + "Results:"
  echo "**********************************************************"
  cd $f
  sqlite3 network_performance.db "SELECT * FROM network_data;"
  cd ..
done

```
change folder variables with ur folder names
and then run it with
```
bash monitor.sh
```

<hr>


Notice that you dont need clone project when u are using Docker

For more information of install project directly click on [Full Documentation](https://github.com/F4RAN/qoe-selenium/blob/main/DOCUMENTATION.md)






