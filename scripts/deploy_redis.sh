#! /bin/bash

### install and setup redis-server ###

# change setting for OS allocation of memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf

# install and setup firewall for Redis
su -c "y" | sudo apt-get install redis-server
rm /etc/redis/redis.conf # remove the original redis.conf file
sudo cp /home/arbiter/buzzz/config/redis/redis.conf /etc/redis/redis.conf # replace the redis.conf file
sudo ufw allow 6379 # open port 6379 for remote access

sudo systemctl restart redis-server

# # ensure background save
# redis-cli bgsave

# disable rdb and enable aof
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config_peepee set appendonly yes
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config_peepee set save ""
