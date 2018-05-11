#! /bin/bash

### SERVER DEPLOY AUTOMATION ###

# STEP 1: change root user password
echo -e "makeitpopwear!1\nmakeitpopwear!1" | passwd root

# STEP 2: create new user and set password
echo -e "projectargogo!\nprojectargogo!" | adduser arbiter
usermod -aG sudo arbiter
groups arbiter

# STEP 3: deploy firewall and allow ports 8000 and OpenSSH
sudo ufw app list
sudo ufw allow OpenSSH
su -c "y" | sudo ufw enable
sudo ufw status
sudo ufw allow 8000

# STEP 4: download PostgreSQL and tweak settings
sudo apt-get update # update OS
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

# DB settings
su -c "psql -c \"CREATE DATABASE arbiter;\"" postgres
su -c "psql -c \"CREATE USER arbiter WITH PASSWORD 'makeitpopweAR!1';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET client_encoding TO 'utf8';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET default_transaction_isolation TO 'read committed';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET timezone TO 'UTC';\"" postgres
su -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE arbiter TO arbiter;\"" postgres

# PostgreSQL localhost setting
cd /etc/postgresql/9.5/main
vim +":%s/#listen_addresses = 'localhost'/listen_addresses = '*'/g | wq" postgresql.conf

cd /etc/postgresql/9.5/main
vim +"%s/127.0.0.1\/32/0.0.0.0\/0   /g | %s/::1\/128/::\/0/g | wq" pg_hba.conf

echo starting PostgreSQL
sudo systemctl start postgresql.service
echo enabling PostgreSQL
sudo systemctl enable postgresql.service
echo restarting PostgreSQL
sudo systemctl restart postgresql.service
# /etc/init.d/postgresql restart
echo done!

# STEP 5: creating python virtual environment for project specific management
export LC_ALL=C
sudo -H pip3 install --upgrade pip
sudo pip3 install setuptools
sudo -H pip3 install virtualenv virtualenvwrapper

echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=/home/arbiter/venv" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

reboot
