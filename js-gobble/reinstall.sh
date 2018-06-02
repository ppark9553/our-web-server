#! /bin/bash

### Gobble.js reinstall ###

# remove existing app
rm -r /home/arbiter/js-gobble

# define the project directory for Gobble.js
mkdir /home/arbiter/js-gobble
sudo cp /home/arbiter/buzzz/js-gobble/* /home/arbiter/js-gobble
sudo chown -R arbiter:arbiter /home/arbiter/js-gobble

# install all Node.js dependencies
cd /home/arbiter/js-gobble
npm install
