#!/bin/bash

# stop and remove existing containers
docker-compose down

# remove existing images
docker images | grep "tsignal" | awk '{print $3}' | xargs docker rmi

# pull latest code from git repository
git pull

# build new image
docker build -t tsignal .

# start containers
docker-compose up -d
