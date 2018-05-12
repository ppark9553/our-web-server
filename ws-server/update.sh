#! /bin/bash
# Docker updater
# @Author  wonseok
# @date    2017/1/15
# @details finding better way (now)


# update images
docker-compose up -d --no-deps --build nginx
docker-compose up -d --no-deps --build app

# re-build images
docker build --tag node-nginx:test .
cd nginx
docker build --tag node-nginx-lb:test .
cd ../

# run compose up
docker-compose up -d
