from machine import Pin
import utime

sensor1 = Pin(14, Pin.IN)
sensor2 = Pin(15, Pin.IN)
while True:
    data1 = str(sensor1.value())
    data2 = str(sensor2.value())
    print('Data1: ' + data1 + ' Data2: ' + data2)
    utime.sleep(.5)