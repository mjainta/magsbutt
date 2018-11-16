import machine
import utime

from umqtt.robust import MQTTClient


def interruptfired(pin):
    if led1.value() == 0:
        led1.value(0)
        print("BUTTON PRESS")
        topic = 'tradebyte/dev/rooms/batman/magsbutt/incr'
        value = 'batman'
        client.publish(topic, value)
        print("PUBLISHED")
        print('{topic}: {value}'.format(topic=topic, value=value))
        print('TIME {0}'.format(utime.time()))
    else:
        led1.value(1)
        print("BUTTON VALUE 1")

led1 = machine.Pin(2, machine.Pin.OUT)
btn1 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

client = MQTTClient('esp-batman', 'MQTT-BROKER-SERVER')
client.connect()

btn1.irq(trigger=machine.Pin.IRQ_RISING, handler=interruptfired)
