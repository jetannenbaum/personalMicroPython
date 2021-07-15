from machine import Pin
import utime

sensor = Pin(15, Pin.IN)
while True:
    data = str(sensor.value())
    print(data)
    utime.sleep(.5)