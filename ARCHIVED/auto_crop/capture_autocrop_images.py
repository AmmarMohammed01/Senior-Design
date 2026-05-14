import cv2 as cv

import board
import neopixel
import json

PIXEL_PIN_TOP = board.D12
NUM_PIXELS = 16
BRIGHTNESS = 0.3
WHITE_COLOR = (255,255,255)
NO_COLOR = (0,0,0)

top_pixels = neopixel.NeoPixel(
    PIXEL_PIN_TOP,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)
def turn_on():
    top_pixels.fill(WHITE_COLOR)
    top_pixels.show()

def turn_off():
    top_pixels.fill(NO_COLOR)
    top_pixels.show()

camera_index = 0

cap = cv.VideoCapture(camera_index)

cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


current_w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
current_h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
print(f"Current Resolution: {int(current_w)}x{int(current_h)}")

LIGHT_ON = False

image_num = 1

def num_read():
    with open('num.json', "r") as f:
        image_num = json.load(f)
        return image_num

def num_write(image_num):
    with open('num.json', "w") as f:
        json.dump(image_num, f)

image_num = num_read()

while True:
    filename = str(image_num) + '.jpg'
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame.")
        break

    cv.imshow('Capture', frame)

    key = cv.waitKey(1)

    if key == ord('c'):
        print(f'Image Captured {filename}')
        cv.imwrite(filename, frame)
        image_num += 1
        num_write(image_num)

    if key == ord('l'):
        LIGHT_ON = not LIGHT_ON
        if LIGHT_ON:
            turn_on()
        else:
            turn_off()

    if key == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
for i in range(4):
    cv.waitKey(1)
