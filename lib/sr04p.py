from machine import Pin, SPI
import utime
import ssd1306

# Define the pins for SPI Clock and Transmit
spi_sck = Pin(2)
spi_tx = Pin(3)
spi = SPI(0, baudrate=100000, sck=spi_sck, mosi=spi_tx)

# Define the pins for Chip Select, DC (Command), and Reset
CS = Pin(1)
DC = Pin(4)
RES = Pin(5)

oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# Turn all pixels off
oled.fill(0)
oled.show()

trigger = Pin(9, Pin.OUT)
echo = Pin(8, Pin.IN)

def ultra():
    signalon = 0
    signaloff = 0
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance

while True:
    oled.fill(0)
    distance = round(ultra() * .254, 2)
    oled.text('Distance: ' + str(distance), 0, 0, 1)
    oled.show()
    utime.sleep(.25)