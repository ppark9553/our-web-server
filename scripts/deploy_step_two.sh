#! /bin/bash

### SERVER DEPLOY AUTOMATION PART 2 ###

mkdir /home/arbiter/buzzz
mv ~/our-web-server/* /home/arbiter/buzzz
rm -r ~/our-web-server

cd /home/arbiter/buzzz

# STEP 1: set up python environment for Django app (should be in virtualenv)
pip install -r /home/arbiter/buzzz/requirements.txt

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

### optional for some ###
# STEP 6: install and setup redis-server
sudo apt-get install redis-server
sudo ufw allow 6379
rm /etc/redis/redis.conf
sudo cp /home/arbiter/buzzz/config/redis/redis.conf /etc/redis/redis.conf
sudo systemctl restart redis-server

# STEP 7: configuring supervisor and firing up celery/celerybeat workers
sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user arbiterbroker 'projectargogo'
sudo rabbitmqctl set_user_tags arbiterbroker administrator
sudo rabbitmqctl set_permissions arbiterbroker ".*" ".*" ".*"
sudo systemctl restart rabbitmq-server

sudo ufw allow 5672

sudo apt-get install supervisor
sudo service supervisor start

sudo mkdir -p /var/log/celery
sudo touch /var/log/celery/arbiter_worker.log
sudo touch /var/log/celery/arbiter_beat.log

sudo cp /home/arbiter/buzzz/config/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
sudo cp /home/arbiter/buzzz/config/supervisor/celerybeat.conf /etc/supervisor/conf.d/celerybeat.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo service supervisor start
