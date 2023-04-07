#!/bin/bash

# check for changes in the git repository
if [ -n "$(git diff --exit-code)" ]; then
  # if there are changes, stop and remove existing containers
  docker-compose down

  # remove existing images
  docker images | grep "tsignal" | awk '{print $3}' | xargs docker rmi

  # pull latest code from git repository
  git pull

  # build new image
  docker build -t tsignal .
else
  # if there are no changes, do nothing
  echo "No changes in git repository, skipping build and deploy."
fi

# start containers
docker-compose up -d