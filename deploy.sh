#!/bin/bash

# change working directory to your Git repository directory
cd /home/Tsignal

# check if there are changes in the Git repository
if [ -n "$(git diff --exit-code)" ]; then
  # if there are changes, stop and remove existing containers
  docker-compose down

  # remove existing images
  docker images | grep "tsignal" | awk '{print $3}' | xargs docker rmi

  # pull latest code from Git repository
  git pull

  # build new image
  docker build -t tsignal .
else
  # if there are no changes, do nothing
  echo "No changes in Git repository, skipping build and deploy."
fi

# start containers
docker-compose up -d

chmod u+x /home/Tsignal/deploy.sh