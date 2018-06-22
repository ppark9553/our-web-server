#! /bin/bash

# backup script for legacy server: 45.32.249.71

# Backing up Django DB

### 1. OHLCV
su arbiter -c "psql -c \"\copy stockapi_ohlcv (date, code, open_price, high_price, low_price, close_price, volume) to '/home/arbiter/backup/ohlcv.csv' delimiter ',';\""
echo OHLCV backup successful
