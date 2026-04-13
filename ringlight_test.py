import time
import board
import neopixel

# Configuration
PIXEL_PIN = board.D18   # GPIO18
NUM_PIXELS = 16
BRIGHTNESS = 0.3        # 0.0 to 1.0

# Initialize NeoPixel
pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)

# Function: set all LEDs to one color
def set_all(color):
    pixels.fill(color)
    pixels.show()

# Function: color wipe animation
def color_wipe(color, delay=0.05):
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(delay)

# Function: rainbow cycle
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait=0.01):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# Main loop
try:
    while True:
        set_all((255, 0, 0))  # Red
        time.sleep(1)

        set_all((0, 255, 0))  # Green
        time.sleep(1)

        set_all((0, 0, 255))  # Blue
        time.sleep(1)

        color_wipe((255, 255, 255))
        time.sleep(1)

        rainbow_cycle()

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
