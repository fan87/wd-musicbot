FROM ubuntu
RUN DEBIAN_FRONTEND="noninteractive" apt update
RUN DEBIAN_FRONTEND="noninteractive" apt install nano -y
RUN DEBIAN_FRONTEND="noninteractive" apt install python3 -y
RUN DEBIAN_FRONTEND="noninteractive" apt install python3-pip -y
RUN DEBIAN_FRONTEND="noninteractive" apt install ffmpeg -y
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /WDMusicBot/
ENTRYPOINT ["/bin/bash", "WDMusicBot/debug.sh"]