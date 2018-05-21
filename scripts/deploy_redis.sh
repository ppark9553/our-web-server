#! /bin/bash

### install and setup redis-server ###

sudo apt-get install redis-server
rm /etc/redis/redis.conf # remove the original redis.conf file
sudo cp /home/arbiter/buzzz/config/redis/redis.conf /etc/redis/redis.conf # replace the redis.conf file
sudo mkdir -p /data/redisdb
sudo chown -R redis:redis /data
### CONFIG SET dir /data/redisdb
### CONFIG SET dbfilename redisdb.rdb
### BGSAVE
sudo systemctl restart redis-server

sudo ufw allow 6379
