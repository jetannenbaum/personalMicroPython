import machine
import ssd1306

spi_sck=machine.Pin(2)
spi_tx=machine.Pin(3)

spi=machine.SPI(0,baudrate=100000,sck=spi_sck, mosi=spi_tx)

CS = machine.Pin(1)
DC = machine.Pin(4)
RES = machine.Pin(5)

oled = ssd1306.SSD1306_SPI(128, 64, spi, DC, RES, CS)

ICON = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

oled.fill(0) # Clear the display
for y, row in enumerate(ICON):
    for x, c in enumerate(row):
        oled.pixel(x + 80, y, c)    

oled.text ('Hello Jet', 0, 0, 1)
oled.show()

# .scroll(x, y)
oled.scroll(10, 10)
oled.show()

oled.scroll(20, 20)
oled.show()