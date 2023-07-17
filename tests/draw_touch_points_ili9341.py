from adafruit_rgb_display.ili9341 import ILI9341
from busio import SPI
from digitalio import DigitalInOut, Direction
import board
from PIL import Image, ImageDraw, ImageFont
import time
from XPT2046_asukiaaa_python.xpt2046 import XPT2046

# Pin Configuration
pin_cs_lcd = DigitalInOut(board.D1)
pin_dc = DigitalInOut(board.D25)
pin_rst = DigitalInOut(board.D24)
pin_led = DigitalInOut(board.D23)
pin_cs_touch = DigitalInOut(board.D7)

# Trun on LED of back panel
pin_led.direction = Direction.OUTPUT
pin_led.value = True

# Set up SPI bus
spi = SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Create the ILI9341 display:
display = ILI9341(
    spi,
    cs=pin_cs_lcd, dc=pin_dc, rst=pin_rst,
    width=240, height=320,
    rotation=90,
    baudrate=24000000
)

# Define colors and fonts
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
# COLOR_GREEN = (0, 206, 69)
COLOR_BLUE = (0, 0, 255)
COLOR_GRAY = (50, 50, 50)
COLOR_WHITE_GRAY = (200, 200, 200)
FONT_DEFAULT = ImageFont.load_default()
# FONT_NOTO_18 = ImageFont.truetype("NotoSansCJK-Regular.ttc", 18)

rect_detect = [(50, 50), (150, 150)]

# Fill display with one color and show text
image = Image.new("RGB", (display.height, display.width) if display.rotation %
                  180 == 90 else (display.width, display.height), COLOR_BLACK)
draw = ImageDraw.Draw(image)
draw.text((10, 5), "hello", COLOR_GREEN, FONT_DEFAULT)
draw.rectangle(rect_detect, outline=COLOR_GRAY)
display.image(image)

# Create touch driver
touch = XPT2046(spi, cs=pin_cs_touch, rotation=display.rotation)

while True:
    touch.update()
    if touch.coordinate is not None or touch.prev_coordinate is not None:
        target_coordinate = touch.coordinate
        color_point = COLOR_WHITE
        if touch.changed_to_press:
            color_point = COLOR_RED
        elif touch.changed_to_release:
            color_point = COLOR_BLUE
            target_coordinate = touch.prev_coordinate
        (x, y) = target_coordinate
        r = 2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color_point)
        color_rect = COLOR_GRAY
        if touch.is_in_rect(rect_detect):
            color_rect = COLOR_WHITE_GRAY
        elif touch.changed_to_release and touch.prev_was_in_rect(rect_detect):
            color_rect = COLOR_GREEN
        draw.rectangle(rect_detect, outline=color_rect)
        display.image(image)
    time.sleep(.01)
