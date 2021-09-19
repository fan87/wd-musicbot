cp --force DockerFiles/Release ./Dockerfile
docker container rm -f $(docker ps -a -q)
docker build -t wdmusic .
docker run -it wdmusic:latest