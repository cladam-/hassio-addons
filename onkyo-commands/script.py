#!/usr/bin/python3

import sys

import eiscp
import paho.mqtt.client as mqtt

print("Starting client")

onkyo_host = sys.argv[1]
mqtt_host = sys.argv[2]

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    receiver = eiscp.eISCP(onkyo_host)
    receiver.command(str(message.payload.decode("utf-8")))
    receiver.disconnect()

client = mqtt.Client("onkyo-commander")

client.on_message=on_message

client.username_pw_set("onkyo", "onkyo")
client.connect(host=mqtt_host)

client.subscribe('onkyo/command')

client.loop_forever()
