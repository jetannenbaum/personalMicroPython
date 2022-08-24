import time
import network
import socket
from machine import Pin
import uasyncio as asyncio
import bitmapfont
import utime
from neopixel import NeoPixel
import secrets


# Configuration:
SPEED          = 10.0    # Scroll speed in pixels per second.
NEOPIXEL_PINS  = [12, 13, 14, 15, 16, 17, 18, 19]  #Pins for the neopixel displays
ROWS           = 8  # Each display has 8 pixels
COLS           = 8  # There are 8 neopixel modules
strips         = [] # a list of neopixel strips
html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W Text Scrolling</h1>
        <p>%s</p>
    </body>
</html>
"""

def write_pixel_value(x, y, value):
    if y >= 0 and y < ROWS and x >=0 and x < COLS:
        strips[x][ROWS - 1 - y] = value

def fill(value):
    for x in range(COLS):
        for y in range(ROWS):
            write_pixel_value(x, y, value)

def show():
    for i in range(COLS):
        strips[i].write()
    
def write_pixel(x, y):
    write_pixel_value(x, y, (1,4,1))

async def scroll_text(message):
    with bitmapfont.BitmapFont(ROWS, COLS, write_pixel) as bf:
        # Global state:
        pos = ROWS                 # X position of the message start.
        message_width = bf.width(message)   # Message width in pixels.
        last = utime.ticks_ms()             # Last frame millisecond tick time.
        speed_ms = SPEED / 1000.0           # Scroll speed in pixels/ms.
        # Main loop:
        while pos > -message_width:
            # Compute the time delta in milliseconds since the last frame.
            current = utime.ticks_ms()
            delta_ms = utime.ticks_diff(current, last)
            last = current
            
            # Compute position using speed and time delta.
            pos -= speed_ms*delta_ms
                
            # Clear the matrix and draw the text at the current position.
            fill((0,0,0))
            bf.text(message, int(pos), 0)
            
            # Update the pixels.
            show()

def connect_to_network():
    global ip
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        ip = str(wlan.ifconfig()[0])
        print( 'ip = ' + ip )

async def serve_client(reader, writer):
    request_line = await reader.readline()

    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    stateis = ''
    try:
        request = str(request_line)
        msg = request.split(' ')[1].split('/')
        if str(msg[1]) == 'msg':
            stateis = str(msg[2]).replace('%20', ' ')
    except:
        print( 'Invalid request: ' + request)
        stateis = error_message

    response = html % stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    await scroll_text(stateis)

async def main():
    global error_message
    onboard = Pin("LED", Pin.OUT, value=0)
    
    for neopixel_pin in NEOPIXEL_PINS:
        strips.append(NeoPixel(Pin(neopixel_pin), ROWS))
    
    fill((0,0,0))
    show()

    print('Connecting to Network...')
    connect_to_network()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    print('Scrolling directions...')
    error_message = "Try: http://" + ip + "/msg/Your Message"
    await scroll_text(error_message)
    print('Ready!')
    while True:
        onboard.on()
        await asyncio.sleep(0.25) 
        onboard.off()
        await asyncio.sleep(5)


for neopixel_pin in NEOPIXEL_PINS:
    strips.append(NeoPixel(Pin(neopixel_pin), ROWS))
    
fill((0,0,0))
show()
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
    