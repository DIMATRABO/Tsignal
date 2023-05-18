#!/bin/bash

# change working directory to your Git repository directory
#cd /home/Tsignal/gitRepo

# fetch the latest changes from remote repository
git fetch


#if [ $(git status -uno | grep 'Your branch is behind' | wc -l) -eq 0 ]; then
if false; then

  # if there are no changes, do nothing
  echo "No changes in Git repository, skipping build and deploy."
 
else

   echo "Changes detected"
   # if there are changes, stop and remove existing containers
  docker-compose down

  # remove existing images
  docker images | grep "tsignal" | awk '{print $3}' | xargs docker rmi

  # pull latest code from Git repository
  #git stash

  git pull

  # build new image
  docker build -t tsignal .

  # start containers
  docker-compose up -d

fi
