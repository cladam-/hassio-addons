#!/usr/bin/with-contenv bashio

onkyoip=$(bashio::config "onkyoip")
mqttip=$(bashio::config "mqttip")
mqttusername=$(bashio::config "mqttusername")
mqttpassword=$(bashio::config "mqttpassword")
mqtttopic=$(bashio::config "mqtttopic")

./script.py $onkyoip $mqttip $mqttusername $mqttpassword $mqtttopic