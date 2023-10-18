FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install packages
RUN apt update && apt install python3-pip python3-venv python3-dev -y

# Install additional packages
RUN apt install wget git iputils-ping lsof -y

# Install ffmpeg
RUN apt install ffmpeg -y

# Install build-essential
RUN apt install build-essential -y

# Install other packages
RUN apt install libavformat-dev libavdevice-dev libavfilter-dev libswscale-dev pkg-config firefox openjdk-11-jdk -y

WORKDIR /tmp

# Clone and build ffmpeg-debug-qp
RUN git clone https://github.com/slhck/ffmpeg-debug-qp.git \
  && cd ffmpeg-debug-qp \
  && make \
  && cp ffmpeg_debug_qp /usr/bin/ffmpeg_debug_qp \
  && chmod +x /usr/bin/ffmpeg_debug_qp

WORKDIR /usr/src/app

# Set up a virtual environment and install Python dependencies
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT python3 ./app.py --file ./aparat_file.txt