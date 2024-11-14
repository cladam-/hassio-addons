#!/usr/bin/with-contenv bashio

ps5ip=$(bashio::config "ps5ip")
username=$(bashio::config "mqttuser")
password=$(bashio::config "mqttpass")
mqtthost=$(bashio::config "mqtthost")
mqttport=$(bashio::config "mqttport")

echo RUN
./ps5.py $ps5ip $mqtthost $mqttport $username $password