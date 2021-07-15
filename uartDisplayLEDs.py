from machine import Pin, UART, I2C
from ssd1306 import SSD1306_I2C
import utime

def readUartBytes(uart, delay=1000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<delay:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    return resp.decode()

print("setting up LEDs")
green = Pin(18, Pin.OUT)
yellow = Pin(19, Pin.OUT)
red = Pin(20, Pin.OUT)

green.high()
yellow.high()
red.high()

# Create the UART
uart0 = UART(id=1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Create the Display object
i2cDisplay=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2cDisplay)

# Print a command line
print("-"*50)
print("Ready to read the UART")

# Loop
y = 0
while True:
    print("reading data")
    data = readUartBytes(uart=uart0)
    if data != "":
        if y == 0:
            oled.fill(0)
        oled.text(data, 0, y)
        oled.show()
        
        data = data.lower()
        if data == 'red':
            green.high()
            yellow.high()
            red.low()
        elif data == 'yellow':
            green.high()
            yellow.low()
            red.high()
        elif data == 'green':
            green.low()
            yellow.high()
            red.high()
        elif data == 'off':
            green.high()
            yellow.high()
            red.high()

        y = y + 10
        if y > 60:
            y = 0
