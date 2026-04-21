import board
import neopixel

# Configuration
PIXEL_PIN_TOP = board.D18   # GPIO18 - Top Ringlight
PIXEL_PIN_BOTTOM = board.D12 # GPIO12 - Bottom Ringlight
NUM_PIXELS = 16
BRIGHTNESS = 0.1        # 0.0 to 1.0

# Color constants
WHITE_COLOR = (255,255,255)
NO_COLOR = (0,0,0)

# Initialize NeoPixel
top_pixels = neopixel.NeoPixel(
    PIXEL_PIN_TOP,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)

bottom_pixels = neopixel.NeoPixel(
    PIXEL_PIN_BOTTOM,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)

def turn_on(light_name: str):
    '''Light name = "top" or "bottom"'''
    if light_name == "top":
        top_pixels.fill(WHITE_COLOR)
        top_pixels.show()
    elif light_name == "bottom":
        bottom_pixels.fill(WHITE_COLOR)
        bottom_pixels.show()

def turn_off(light_name: str):
    '''Light name = "top" or "bottom"'''
    if light_name == "top":
        top_pixels.fill(NO_COLOR)
        top_pixels.show()
    elif light_name == "bottom":
        bottom_pixels.fill(NO_COLOR)
        bottom_pixels.show()

