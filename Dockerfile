FROM python:3.8

WORKDIR /usr/src/app

# install chromium
RUN apt install --assume-yes chromium-browser

# install java
RUN apt-get install -y default-jre

# install chromedriver
RUN apt-get install chromium-chromedriver

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install qoe-selenium project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT python ./app.py