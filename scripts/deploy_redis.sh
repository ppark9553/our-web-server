#! /bin/bash

### install and setup redis-server ###

sudo apt-get install redis-server
rm /etc/redis/redis.conf # remove the original redis.conf file
sudo cp /home/arbiter/buzzz/config/redis/redis.conf /etc/redis/redis.conf # replace the redis.conf file
sudo ufw allow 6379 # open port 6379 for remote access

sudo systemctl restart redis-server
