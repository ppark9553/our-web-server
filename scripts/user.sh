#! /bin/bash

### SERVER DEPLOY AUTOMATION ###

# STEP 1: create new user and set password
echo -e "projectargogo!\nprojectargogo!" | adduser arbiter
usermod -aG sudo arbiter
