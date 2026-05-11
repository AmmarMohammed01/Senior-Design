'''
RESULTS (notice how it skips camera index 1)
0: height 1080.0, width 1920.0
2: height 1080.0, width 1920.0
'''
import cv2 as cv

for camera_index in [0,2]:
    capture = cv.VideoCapture(camera_index)
    capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    print(f"{camera_index}: height {h}, width {w}")
    capture.release()

