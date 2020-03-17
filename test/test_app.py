#!/usr/bin/env python
# -*- coding: utf-8 --
"""Test webapp

Usage:
    python test_app.py

"""
from datetime import datetime

import paho.mqtt.client as mqtt
import json
import time


CLIENT_ID = 'test-app'

# MQTT broker
# MQTT_BROKER_HOST = 'localhost'
MQTT_BROKER_HOST = '192.168.0.118'
MQTT_BROKER_PORT = 1883

# connection parameters
MQTT_BROKER_RETRY_ATTEMPT = 5 # number of retry attempts
MQTT_BROKER_RETRY_TIMEOUT = 10 # [seconds]

# topics
TOPIC_ALL = 'temi/+/command/#'

def on_connect(client, userdata, flags, rc):
    """Connect to MQTT broker and subscribe to topics

    """
    print("Successfully connected to {}:{} (rc:{})".format(MQTT_BROKER_HOST, MQTT_BROKER_PORT, str(rc)))

    # list of subscribed topics
    client.subscribe(topic=TOPIC_ALL, qos=0)


def on_disconnect(client, userdata, rc):
    """Disconnect from MQTT broker

    """
    print("Disconnected from {}:{} (rc:{})".format(MQTT_BROKER_HOST, MQTT_BROKER_PORT, str(rc)))
    client.loop_stop()


def on_message(client, log_filename, message):
    """Generic message callback

    """
    print("[{}] {}".format(datetime.now(), message.topic))
    print("{}".format(message.payload))


if __name__ == '__main__':
    # create a new MQTT client instance
    client = mqtt.Client(client_id=CLIENT_ID)

    # attach callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add(TOPIC_ALL, on_message)

    # connect to MQTT broker
    print("Connecting to {}:{}".format(MQTT_BROKER_HOST, MQTT_BROKER_PORT))
    client.connect(
        host = MQTT_BROKER_HOST,
        port = MQTT_BROKER_PORT,
        keepalive = 60,
        bind_address = "")

    # start listening to topics
    client.loop_start()

    # time.sleep(0.5)
    while True:
        # status messages
        print("[{}] Publish Status".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
        client.publish('temi/00119452440/status/info', json.dumps({
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'battery_percentage': 50,
            'waypoint_list': ['home base', 'a', 'b', 'c'], 
            }), qos=0)
        time.sleep(1)

        print("[{}] Publish Status".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
        client.publish('temi/00119462420/status/info', json.dumps({
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'battery_percentage': 95,
            'waypoint_list': ['home base', 'd', 'e', 'f'], 
            }), qos=0)
        time.sleep(1)

        # command messages
        print("[{}] Publish Command".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
        client.publish('temi/00119452440/command/move/forward', json.dumps({
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'battery_percentage': 50,
            'waypoint_list': ['home base', 'a', 'b', 'c'], 
            }), qos=0)
        time.sleep(1)

        print("[{}] Publish Command".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
        client.publish('temi/00119452440/command/move/backward', json.dumps({
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'battery_percentage': 95,
            'waypoint_list': ['home base', 'd', 'e', 'f'], 
            }), qos=0)
        time.sleep(1)
