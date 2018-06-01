#! /bin/bash

### SERVER DEPLOY AUTOMATION ###

# STEP 1: change root user password
echo -e "makeitpopwear!1\nmakeitpopwear!1" | passwd root

# STEP 2: create new user and set password
echo -e "projectargogo!\nprojectargogo!" | adduser arbiter
usermod -aG sudo arbiter

# STEP 3: deploy firewall and allow ports 8000 and OpenSSH
sudo ufw app list
sudo ufw allow OpenSSHfab
su -c "y" | sudo ufw enable

# STEP 4: update
sudo apt-get update # update OS

# moving around code base
cd /home/arbiter
mkdir buzzz
git clone https://github.com/ppark9553/our-web-server.git ./buzzz
# remove the initially pulled repo now
rm -r ~/our-web-server
