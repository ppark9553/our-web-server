#! /bin/bash

### install and setup redis-server ###

# change setting for OS allocation of memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf

# install and setup firewall for Redis
sudo apt-get install redis-server
cd /etc/redis
vim +":%s/# requirepass foobared/requirepass da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065/g | wq" redis.conf

# disable rdb and enable aof
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config set appendonly yes
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config set save ""
