# QoE-Selenium

If you use this repository in your research, please **cite the following paper**:

> **Panahi, P. H. S., Jalilvand, A. H., & Diyanat, A. (2025).**  
> *An efficient network-based QoE assessment framework for multimedia networks using a machine learning approach.*  
> **IEEE Open Journal of the Communications Society**

---

## Prerequisites: Create Required Files (Important)

Before running the project, you **must create a shared directory** containing the following **three mandatory files**:

1. `aparat_file.txt`  
2. `network_performance.db`  
3. `config.txt`

These files are mounted into the Docker container and are required for proper execution.

---

## File Descriptions

### 1. `aparat_file.txt`

This file contains the list of Aparat video records used during testing.

- Copy its contents **exactly** from the official project file:  
  https://github.com/F4RAN/qoe-selenium/blob/main/aparat_file.txt

Paste the records into your local `aparat_file.txt`.

---

### 2. `config.txt`

This file defines **network emulation parameters**.

- On **Windows**, you may leave this file **empty**
- On **Linux**, use it to define traffic control (tc) rules

Each line represents a network constraint. If you do not want a specific limitation, simply remove the corresponding line.

You may also copy **predefined network profiles** from:  
https://github.com/F4RAN/qoe-selenium/blob/main/NETWORKS.md

#### Example: *Good 3G Network*
```txt
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

---

### 3. `network_performance.db`

This SQLite database is automatically populated **during runtime** and stores all collected network and QoE measurements.

---

## Create Files (Single Command)

### Linux
```bash
mkdir /path/to/shared && cd /path/to/shared
touch aparat_file.txt network_performance.db config.txt
```

### Windows
```bat
mkdir C:\shared & cd C:\shared ^
& type nul > aparat_file.txt ^
& type nul > network_performance.db ^
& type nul > config.txt
```

---

## Run the Project (Linux)

### AMD Architecture
```bash
docker run \
-v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt \
-v $(pwd)/network_performance.db:/usr/src/app/network_performance.db \
-v $(pwd)/config.txt:/usr/src/app/config.txt \
--cap-add NET_ADMIN \
--rm -it f4ran/qoe-selenium-amd
```

### ARM Architecture
```bash
docker run \
-v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt \
-v $(pwd)/network_performance.db:/usr/src/app/network_performance.db \
-v $(pwd)/config.txt:/usr/src/app/config.txt \
--cap-add NET_ADMIN \
--rm -it f4ran/qoe-selenium-arm
```

---

## Run the Project (Windows)

```bash
docker run \
-v //c/shared/aparat_file.txt:/usr/src/app/aparat_file.txt \
-v //c/shared/network_performance.db:/usr/src/app/network_performance.db \
-v //c/shared/config.txt:/usr/src/app/config.txt \
--cap-add NET_ADMIN \
--rm -it f4ran/qoe-selenium-amd
```

---

## Server Usage

### Create Files
```bash
mkdir medium-3g
cd medium-3g
touch aparat_file.txt network_performance.db config.txt
```

### Run Container in Detached Mode
```bash
docker run -d --name medium-3g \
-v $(pwd)/aparat_file.txt:/usr/src/app/aparat_file.txt \
-v $(pwd)/network_performance.db:/usr/src/app/network_performance.db \
-v $(pwd)/config.txt:/usr/src/app/config.txt \
--cap-add NET_ADMIN \
--rm -it f4ran/qoe-selenium-amd
```

---

## Documentation

👉 https://github.com/F4RAN/qoe-selenium/blob/main/DOCUMENTATION.md
