from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import time

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
txt = "Temp: {temp:.2f}"


while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperatureC = 27 - (reading - 0.706)/0.001721
    temperatureF = (temperatureC * 9/5) + 29.5 # off by 2.5 degrees
    oled.fill(0)
    oled.text(txt.format(temp = temperatureF) + " F", 0, 0)
    oled.show()
    print(txt.format(temp = temperatureF) + " Degrees F")
    time.sleep(2)
