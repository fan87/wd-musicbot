FROM ubuntu
RUN DEBIAN_FRONTEND="noninteractive" apt update
RUN DEBIAN_FRONTEND="noninteractive" apt install nano -y
RUN DEBIAN_FRONTEND="noninteractive" apt install python3.9 -y
RUN DEBIAN_FRONTEND="noninteractive" apt install python3-pip -y
RUN DEBIAN_FRONTEND="noninteractive" apt install ffmpeg -y
COPY requirements.txt /tmp/
RUN python3.9 -m pip install -r /tmp/requirements.txt
COPY . /WDMusicBot/
RUN DEBIAN_FRONTEND="noninteractive" apt install git -y
RUN git init
RUN git remote add origin https://github.com/fan87/wd-musicbot
ENTRYPOINT ["/bin/bash", "WDMusicBot/debug.sh"]