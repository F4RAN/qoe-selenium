#FROM amd64/ubuntu:18.04
#WORKDIR /usr/src/app
#
#RUN apt update && apt install -y wget curl
## install google chrome
##RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
##RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
##RUN apt-get -y update
##RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
##
##RUN apt-get install -y google-chrome-stable
#RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
#
#
## install java
#RUN apt-get install -y default-jre
#
## install chromedriver
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#
## set display port to avoid crash
#ENV DISPLAY=:99
#
#
## install qoe-selenium project
#
##RUN apt-get install software-properties-common
##RUN add-apt-repository ppa:deadsnakes/ppa -y
##RUN apt-get update
##RUN apt-get install -y python3.9.7
##RUN apt-get install -y python3-pip
#RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
#RUN wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
#RUN tar -xf Python-3.9.7.tgz && cd Python-3.9.7 && ./configure --enable-optimizations && make -j 8 && make altinstall
#
#COPY requirements.txt ./
#RUN pip3.9 install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#ENTRYPOINT python3.9 ./app.py --file ./aparat_file.txt


#FROM selenium/standalone-chrome:latest
FROM seleniarm/standalone-chromium:latest
USER root
WORKDIR /usr/src/app
RUN apt update && apt install python3-pip  python3.11-venv -y  && apt install wget git iputils-ping lsof -y
RUN python3 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#RUN pip3 install --upgrade pip
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN rm -rf /usr/bin/chromedriver
RUN apt install chromium-driver -y
WORKDIR /tmp
RUN wget https://ffmpeg.org/releases/ffmpeg-4.2.2.tar.gz
RUN tar -xzf ffmpeg-4.2.2.tar.gz
WORKDIR /tmp/ffmpeg-4.2.2
RUN apt-get install -y nasm yasm libx264-dev libx265-dev libnuma-dev libvpx-dev libopus-dev
RUN ./configure --disable-asm
RUN make
RUN make install
RUN mv ./ffmpeg /usr/bin/ffmpeg
RUN mv ./ffprobe /usr/bin/ffprobe
WORKDIR /tmp
RUN apt install -y pkg-config
RUN git clone https://github.com/slhck/ffmpeg-debug-qp.git \
  && cd ffmpeg-debug-qp \
  && make \
  && cp ffmpeg_debug_qp /usr/bin/ffmpeg_debug_qp \
  && chmod +x /usr/bin/ffmpeg_debug_qp

WORKDIR /usr/src/app
ENTRYPOINT python3 ./app.py --file ./aparat_file.txt
