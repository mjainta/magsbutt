import configparser
import json
import os
import re

import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config['MQTT']['TOPIC'])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    match = re.match(".+/([a-zA-Z]+)/magsbutt/incr", msg.topic)
    print("{0} vs. {1}".format(match.group(1), msg.payload.decode('utf-8')))

    if match.group(1) == msg.payload.decode('utf-8'):
        log_increase(match.group(1))

def log_increase(room):
    filepath = os.path.abspath(config['ROOMS']['FILENAME'])
    print(filepath)
    if os.path.isfile(config['ROOMS']['FILENAME']):
        room_json = open(filepath).read()
        room_data = json.loads(room_json)
        print("Found file {0}!".format(filepath))
    else:
        room_data = {}
        print("No file {0}!".format(filepath))

    print("Room data before: {room_data}".format(room_data=room_data))

    if room in room_data:
        if 'magsbutt_count' in room_data[room]:
            room_data[room]['magsbutt_count'] = room_data[room]['magsbutt_count'] + 1
        else:
            room_data[room]['magsbutt_count'] = 1
    else:
        room_data[room] = {}
        room_data[room]['magsbutt_count'] = 1

    print("Room {room} count: {count}".format(room=room, count=room_data[room]['magsbutt_count']))
    room_file = open(filepath, 'w')
    room_file.write(json.dumps(room_data))
    room_file.close()


config = configparser.ConfigParser()
config.read('magsbutt.ini')
print(config['MQTT']['SERVER'])
print(config['MQTT']['PORT'])
print(config['MQTT']['TOPIC'])
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config['MQTT']['SERVER'], int(config['MQTT']['PORT']), 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
