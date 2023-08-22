#!/bin/bash

touch /var/log/vasko.log

# Start logging in background
tail -f /var/log/vasko.log &

echo 'Generating crontab' >> /var/log/vasko.log
python -u cron_generator.py vasko-cron

echo 'Installing crontab' >> /var/log/vasko.log
crontab -r
crontab vasko-cron
crontab -l >> /var/log/vasko.log

echo 'Starting cron' >> /var/log/vasko.log
# Start cron daemon and keep container running
cron && tail -f /dev/null
