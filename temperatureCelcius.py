from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def clear(x):
    for j in range(x,63):
        oled.line(x,j - 1,127,j - 1,0)
    oled.show()

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperatureC = 27 - (reading - 0.706)/0.001721
    temperatureF = (temperatureC * 9/5) + 32
    clear(0)
    oled.text("Temp: " + str(temperatureF), 0, 0)
    oled.show()
    print(temperatureF)
    time.sleep(2)
