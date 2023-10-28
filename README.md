## Config file (config.txt):
We use tcconfig to customize network performance to simulate different situations

example: <small>You can find other options for network configuration [Here](https://tcconfig.readthedocs.io/en/latest/pages/usage/tcset/index.html)</small>
```
rate 100Kbps # Network bandwidth rate [G/M/K bps]
delay 100ms # Network latency [microseconds/milliseconds/seconds/minutes]
loss 0.1% # Packet loss rate [%]
duplicate -1 # Packet corruption rate [%]
corrupt -1 # Packet corruption rate [%]
reordering -1 # Packet reordering rate [%]
shaping-algo -1 # {htb,tbf}
direction -1 # {outgoing,incoming}

```
<b>-1 means not set<b>

## Installation/Run scenario on Docker
At first you must to create shared folder with 2 files: 1- aparat_file.txt, 2- network_performance.db

in Unix-based systems:
```
mkdir /path/to/shared/ && cd /path/to/shared/
touch aparat_file.txt
touch network_performance.db
touch config.txt
```
in Windows systems:

```
mkdir C:\shared 
cd C:\shared
type nul > aparat_file.txt
type nul > network_performance.db
type nul > config.txt
```

edit aparat_file.txt and put an Aparat video link in the each line

then run the project with the bottom line:
```
docker run -v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt -v $(pwd)/network_performance.db:/usr/src/app/network_performance.db -v $(pwd)/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
# For arm architecture use f4ran/qoe-selenium-arm
```

for windows systems:
```
docker run -v //c/shared/aparat_file.txt:/usr/src/app/aparat_file.txt -v //c/shared/network_performance.db:/usr/src/app/network_performance.db -v //c/shared/config.txt:/usr/src/app/config.txt --cap-add NET_ADMIN --rm -it f4ran/qoe-selenium-amd
# For arm architecture use f4ran/qoe-selenium-arm

```
network_performance.db update live when application is running.

