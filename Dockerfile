# FROM python:3.8
FROM --platform=linux/amd64 python:3.8

WORKDIR /usr/src/app

# install chromium
RUN apt-get update
RUN apt-get install -y  chromium

# install java
RUN apt-get install -y default-jre

# install chromedriver
# RUN wget -O /tmp/chrome-driver.deb http://ftp.tw.debian.org/debian/pool/main/c/chromium/chromium-driver_113.0.5672.126-1_amd64.deb
# RUN dpkg -i  /tmp/chromium-driver.deb
RUN apt-get install -y chromium-driver

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install qoe-selenium project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT python ./app.py