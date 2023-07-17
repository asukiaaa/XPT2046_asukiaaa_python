from XPT2046_asukiaaa_python.xpt2046 import XPT2046
import board
import busio
from digitalio import DigitalInOut
from time import sleep

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs = DigitalInOut(board.D7)
touch = XPT2046(spi, cs)

print("start monitoring touch")

while True:
    touch.update()
    if touch.coordinate is not None:
        print(touch.coordinate)
    sleep(.01)
