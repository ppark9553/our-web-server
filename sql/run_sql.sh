#! /bin/bash

### SETTING UP TRIGGERS ###

psql -d arbiter -a -f /home/arbiter/buzzz.co.kr/sql/trigger.sql
