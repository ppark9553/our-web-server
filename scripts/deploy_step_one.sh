#! /bin/bash

### SERVER DEPLOY AUTOMATION ###

# STEP 1: change root user password
echo -e "makeitpopwe123ARbiter;;\nmakeitpopwe123ARbiter;;" | passwd root

# STEP 2: create new user and set password
echo -e "projectargogo123alright;;\nprojectargogo123alright;;" | adduser arbiter
usermod -aG sudo arbiter

# STEP 3: deploy firewall and allow ports 8000 and OpenSSH
sudo ufw app list
sudo ufw allow OpenSSH
su -c "y" | sudo ufw enable

# STEP 4: download PostgreSQL and tweak settings
sudo apt-get update # update OS
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib

# DB settings
su -c "psql -c \"CREATE DATABASE arbiter;\"" postgres
su -c "psql -c \"CREATE USER arbiter WITH PASSWORD 'makeitpopwe123arBITER!1';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET client_encoding TO 'utf8';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET default_transaction_isolation TO 'read committed';\"" postgres
su -c "psql -c \"ALTER ROLE arbiter SET timezone TO 'UTC';\"" postgres
su -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE arbiter TO arbiter;\"" postgres

# PostgreSQL localhost setting
cd /etc/postgresql/9.5/main
vim +":%s/#listen_addresses = 'localhost'/listen_addresses = '*'/g | wq" postgresql.conf

cd /etc/postgresql/9.5/main
vim +"%s/127.0.0.1\/32/0.0.0.0\/0   /g | %s/::1\/128/::\/0/g | wq" pg_hba.conf

sudo systemctl enable postgresql.service
sudo systemctl restart postgresql.service

sudo ufw allow 5432

# PART 2: other dependencies #
# now with the database set up, pull your github repo into your server again
cd /home/arbiter
mkdir buzzz
git clone https://github.com/ppark9553/our-web-server.git ./buzzz
# remove the initially pulled repo now
rm -r ~/our-web-server

# STEP 5: download uwsgi and nginx
sudo apt-get install build-essential nginx
sudo apt-get install uwsgi uwsgi-emperor uwsgi-plugin-python3
sudo -H pip3 install uwsgi

sudo usermod -aG www-data arbiter

# STEP 6: copy and paste configuration files for uwsgi and nginx
sudo mkdir -p /etc/uwsgi/sites
sudo cp /home/arbiter/buzzz/config/uwsgi/buzzz.ini /etc/uwsgi/sites/buzzz.ini
# finish up on the uwsgi setting by configuring uwsgi-emperor
sudo ln -s /etc/uwsgi/sites/buzzz.ini /etc/uwsgi-emperor/vassals # link your .ini file with emperor's vassals
sudo cp /home/arbiter/buzzz/config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service

sudo cp /home/arbiter/buzzz/config/nginx/buzzz.conf /etc/nginx/sites-available/buzzz.conf
sudo ln -s /etc/nginx/sites-available/buzzz.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start uwsgi

# STEP 7: changing firewall options
sudo ufw allow 'Nginx Full'

# STEP 8: last step configuring uwsgi and nginx
sudo systemctl enable nginx
sudo systemctl enable uwsgi

### last step ###
# STEP 9: creating python virtual environment for project specific management
sudo -H pip3 install --upgrade pip
sudo pip3 install setuptools
sudo -H pip3 install virtualenv virtualenvwrapper

echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=/home/arbiter/venv" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

reboot
