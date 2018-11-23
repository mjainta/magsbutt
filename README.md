# magsbutt

My ass got saved by using tests today.

# How to set it up

Pre-requisites:
* An ESP32 with a button connected to D21 (Pin21 internally)
* A MQTT broker, your laptop is sufficient (for example mosquitto)
* Python3 installed
* A WLAN network in which the ESP, the MQTT broker and MQTT client are in
* Downloaded firmware for micropython and the ESP32 board (http://micropython.org/download)

Setting up the ESP
```bash
# Setup project environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Flash ESP32 and install micropython firmware
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin

# Prepare magsbutt.ini
cp magsbutt.example.ini magsbutt.ini
```

# Run the system

Only for debugging / logging - Subscribe as a client to the MQTT broker
```bash
mosquitto_sub -v -h localhost -p 1883 -t '#'
```

Ramp up the ESP32
```bash
rshell --port /dev/ttyUSB0
cp boot.py /pyboard/boot.py
cp main.py /pyboard/main.py
repl
```

Ramp up the python MQTT client
```bash
python3 client.py
```

Now, push the button and look at your terminals.

# Using the ELK stack

You probably need to change the max_map_count setting of your system

```bash
sudo sysctl -w vm.max_map_count=262144
```

Then start the ELK stack in docker containers
```bash
docker run --rm -e MAX_MAP_COUNT=262144 -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --name elk sebp/elk
```
