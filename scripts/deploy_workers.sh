#! /bin/bash

### onfiguring supervisor and firing up celery/celerybeat workers ###

# STEP 1: install and configure RabbitMQ
sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user arbiterbroker 'projectargogo'
sudo rabbitmqctl set_user_tags arbiterbroker administrator
sudo rabbitmqctl set_permissions arbiterbroker ".*" ".*" ".*"
sudo systemctl restart rabbitmq-server

sudo ufw allow 5672

# STEP 2: install supervisor and daemonize celery workers/celerybeat
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
