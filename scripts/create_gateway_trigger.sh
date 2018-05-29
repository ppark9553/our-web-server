#! /bin/bash

##### create gateway SQL triggers #####
su -c "psql -d arbiter -a -f /home/arbiter/buzzz/sql/gateway_trigger.sql" postgres
echo Gateway trigger created

sudo systemctl restart postgresql
