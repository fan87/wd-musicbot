FROM ubuntu
RUN apt update
RUN apt install nano -y
RUN apt install python3 -y
RUN apt install python3-pip -y
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /WDMusicBot/
RUN rm -r /WDMusicBot/run
ENTRYPOINT ["/bin/bash", "WDMusicBot/run.sh"]