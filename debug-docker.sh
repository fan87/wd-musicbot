cp --force DockerFiles/Debug ./Dockerfile
docker container rm -f $(docker ps -a -q)
docker build -t wdmusic-debug .
docker run -it wdmusic-debug:latest