#!/usr/bin/python3

import subprocess
import sys
import paho.mqtt.client as mqtt
import schedule
import time

ps5_host = sys.argv[1]
mqtt_host = sys.argv[2]
mqtt_port = sys.argv[3]
mqtt_usr = sys.argv[4]
mqtt_pass = sys.argv[5]


def check_ps5_status():
    p1 = subprocess.Popen(['echo', '"SRCH * HTTP/1.1"'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["nc", "-u", '-w4', ps5_host, '9302'], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    output = p2.communicate()[0]

    if('620' in str(output)):
        client.publish('homeassistant/binary_sensor/ps5mqtt/state', 'OFF')
    elif('200' in str(output)):
        client.publish('homeassistant/binary_sensor/ps5mqtt/state', 'ON')
    else:
        client.publish('homeassistant/binary_sensor/ps5mqtt/state', 'OFF')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "ps5-status")

client.username_pw_set(mqtt_usr, mqtt_pass)
client.connect(host=mqtt_host)

client.publish('homeassistant/binary_sensor/ps5mqtt/config', '{\"id\":\"ps5_check\",\"unique_id\":\"ps5_check\",\"name\":\"PlayStation 5\",\"state_topic\":\"homeassistant/binary_sensor/ps5mqtt/state\"}')

schedule.every(5).seconds.do(check_ps5_status)

while True:
    schedule.run_pending()
    time.sleep(1)
