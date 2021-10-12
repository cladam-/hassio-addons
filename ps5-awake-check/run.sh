#!/usr/bin/with-contenv bashio

username=$(bashio::config "mqttuser")
password=$(bashio::config "mqttpass")
mqtthost=$(bashio::config "mqtthost")
mqttport=$(bashio::config "mqttport")

mosquitto_pub -h "$mqtthost" -p "$mqttport" -u "$username" -P "$password" -t homeassistant/binary_sensor/ps5mqtt/config -m "{\"name\":\"ps5mqtt\",\"state_topic\":\"homeassistant/binary_sensor/ps5mqtt/state\"}"
echo 'Running!'
while true ; do ./script & sleep 5; done