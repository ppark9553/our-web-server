#! /bin/bash

### SERVER DEPLOY AUTOMATION PART 2 ###

mkdir /home/arbiter/buzzz
mv ~/our-web-server/* /home/arbiter/buzzz
rm -r ~/our-web-server
cd /home/arbiter/buzzz

# STEP 1: set up python environment for Django app (should be in virtualenv)
pip install -r ../requirements.txt

# STEP 2: download uwsgi and nginx
sudo apt-get install build-essential nginx
sudo -H pip3 install uwsgi

# STEP 3: copy and paste configuration files for uwsgi and nginx
sudo mkdir -p /etc/uwsgi/sites
sudo cp /home/arbiter/buzzz/config/uwsgi/buzzz.ini /etc/uwsgi/sites/buzzz.ini
sudo cp /home/arbiter/buzzz/config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service

sudo cp /home/arbiter/buzzz/config/nginx/buzzz.conf /etc/nginx/sites-available/buzzz.conf
sudo ln -s /etc/nginx/sites-available/buzzz.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start uwsgi

# STEP 4: changing firewall options
sudo ufw allow 'Nginx Full'

# STEP 5: last step configuring uwsgi and nginx
sudo systemctl enable nginx
sudo systemctl enable uwsgi
