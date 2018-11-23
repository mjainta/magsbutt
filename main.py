import machine
import utime

from umqtt.robust import MQTTClient


def interruptfired(pin):
    if pin.value() == 0:
        led1.value(0)
        print("BUTTON PRESS")
        topic = 'tradebyte/dev/rooms/batman/magsbutt/incr'
        value = 'batman'
        client.publish(topic, value)
        print("PUBLISHED")
        print('{topic}: {value}'.format(topic=topic, value=value))
        print('Pin Value: {0}'.format(pin.value()))
        print('TIME {0}'.format(utime.time()))
    else:
        print("BUTTON VALUE {0}".format(pin.value()))

led1 = machine.Pin(2, mode=machine.Pin.OUT)
btn1 = machine.Pin(21, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

client = MQTTClient('esp-batman', 'MQTT-BROKER-SERVER')
client.connect()

btn1.irq(trigger=machine.Pin.IRQ_FALLING, handler=interruptfired)
