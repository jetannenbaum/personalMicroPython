import machine
import ssd1306
import time

# Takes an input number vale and a range between high-and-low and returns it scaled to the new range
# This is similar to the Arduino map() function
def scaled(value, istart, istop, ostart, ostop):
  return int(ostart + (ostop - ostart) * ((int(value) - istart) / (istop - istart)))

spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)
spi=machine.SPI(0,baudrate=100000,sck=spi_sck, mosi=spi_tx)

CS = machine.Pin(1)
DC = machine.Pin(4)
RES = machine.Pin(5)

oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

# turn all pixels off
oled.fill(0)
oled.show()
oled.text('Etch-A-Sketch', 0, 0, 1)
oled.text('Hit the reset', 0, 20, 1)
oled.text('button to clear', 0, 30, 1)
oled.text('the screen', 0, 40, 1)
oled.show()

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

while button.value() != 1:
    time.sleep(.25)
    
oled.fill(0)
oled.show()

vert = machine.ADC(26)
horiz = machine.ADC(27)

x = newX = scaled(vert.read_u16(), 0, 65536, 0, 128)
y = newY = scaled(horiz.read_u16(), 0, 65536, 0, 64)

while True:
    oled.line(x, y, newX, newY, 1)
    x = newX
    y = newY
    if button.value():
        oled.fill(0)
    oled.show()
    time.sleep(.2)
    newX = scaled(vert.read_u16(), 0, 65536, 0, 128)
    newY = scaled(horiz.read_u16(), 0, 65536, 0, 64)
