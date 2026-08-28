#!/usr/bin/python3

import sys
import logging
import time

import eiscp
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("onkyo-commander")

DEFAULT_ONKYO_HOST = "192.168.1.xxx"
DEFAULT_MQTT_HOST = "core-mosquitto"
DEFAULT_MQTT_USER = ""
DEFAULT_MQTT_PASS = ""
DEFAULT_TOPIC = "onkyo/command"
MQTT_RETRY_SECONDS = 5


def main():
    args = sys.argv[1:] + [""] * 5
    onkyo_host = args[0] or DEFAULT_ONKYO_HOST
    mqtt_host = args[1] or DEFAULT_MQTT_HOST
    mqtt_user = args[2] or DEFAULT_MQTT_USER
    mqtt_pass = args[3] or DEFAULT_MQTT_PASS
    topic = args[4] or DEFAULT_TOPIC

    if not onkyo_host or onkyo_host == "192.168.1.xxx":
        log.error("No onkyoip configured; set the 'onkyoip' add-on option.")
        sys.exit(1)

    receiver = eiscp.eISCP(onkyo_host)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="onkyo-commander")
    if mqtt_user:
        client.username_pw_set(mqtt_user, mqtt_pass)

    def on_message(client, userdata, message):
        try:
            command = message.payload.decode("utf-8").strip()
        except UnicodeDecodeError:
            log.error("Ignoring non-UTF-8 payload from %s", message.topic)
            return
        if not command:
            log.warning("Ignoring empty command")
            return
        log.info("Sending command %r to receiver", command)
        try:
            receiver.command(command)
        except Exception as exc:
            log.error("Failed to send %r: %s", command, exc)
            log.info("Reconnecting to receiver...")
            try:
                receiver.disconnect()
                receiver.command(command)
                log.info("Retry succeeded")
            except Exception as retry_exc:
                log.error("Retry failed for %r: %s", command, retry_exc)

    client.on_message = on_message
    while True:
        try:
            client.connect(host=mqtt_host)
            break
        except Exception as exc:
            log.error("MQTT connect to %s failed: %s (retrying in %ss)", mqtt_host, exc, MQTT_RETRY_SECONDS)
            time.sleep(MQTT_RETRY_SECONDS)

    log.info("Subscribing to %s", topic)
    client.subscribe(topic)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log.info("Shutting down")
        receiver.disconnect()


if __name__ == "__main__":
    main()
