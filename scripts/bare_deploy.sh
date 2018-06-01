#! /bin/bash

### SERVER DEPLOY AUTOMATION ###

# STEP 1: change root user password
echo -e "6bf11c214d3481c681a83a948983e79233cac39150a64bdbc0a043f2d36d362f\n6bf11c214d3481c681a83a948983e79233cac39150a64bdbc0a043f2d36d362f" | passwd root

# STEP 2: create new user and set password
echo -e "bc1504e8a4067f798fb1caed16ecf06716d37d883894e4df8709b7863f3c4368\nbc1504e8a4067f798fb1caed16ecf06716d37d883894e4df8709b7863f3c4368" | adduser arbiter
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
