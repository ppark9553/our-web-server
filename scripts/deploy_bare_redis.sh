#! /bin/bash

### install and setup redis-server ###

# change setting for OS allocation of memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf

# install and setup firewall for Redis
sudo apt-get install redis-server
cd /etc/redis
# bind to all incoming IP addressed and open port 6379
# however, add a password so that only authenticated users can access the cache db
vim +":%s/bind 127.0.0.1/bind 0.0.0.0/g | wq" redis.conf
vim +":%s/# requirepass foobared/requirepass da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065/g | wq" redis.conf
sudo ufw allow 6379
sudo systemctl restart redis-server

# disable rdb and enable aof
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config set appendonly yes
redis-cli -a da56038fa453c22d2c46e83179126e97d4d272d02ece83eb83a97357e842d065 config set save ""
