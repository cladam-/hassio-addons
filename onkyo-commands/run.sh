#!/usr/bin/with-contenv bashio

onkyoip=$(bashio::config "onkyoip")
mqttip=$(bashio::config "mqttip")

./script.py $onkyoip $mqttip