#!/usr/bin/with-contenv bashio

onkyoip=$(bashio::config "onkyoip")
mqttip=$(bashio::config "onkyoip")

./script.py $onkyoip $mqttip