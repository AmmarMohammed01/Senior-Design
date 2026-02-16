# OpenCV Imports
import cv2 as cv
import numpy as np

# SSIM Import
from skimage.metrics import structural_similarity as ssim

"""Take image of GOLDEN board"""

'''
capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = capture.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
capture.release()
cv.destroyAllWindows()

# Let user select ROI (drag a box)
roi = cv.selectROI("Select ROI", frame, False) # tuple: (x,y, width, height)

# Extract cropped region
cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

# Save and display cropped image
cv.imwrite("Board1.png", cropped_img)
'''

"""Take image of TEST board"""

'''
capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = capture.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.rectangle(frame, (roi[0]-5, roi[1]-5), (roi[0]+roi[2]+5, roi[1]+roi[3]+5), (0, 255, 0), 5)

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# Extract cropped region
cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

# Save and display cropped image
cv.imwrite("Board2.png", cropped_img)

# When everything done, release the capture
capture.release()
cv.destroyAllWindows()

'''

"""Compare two boards"""
# board1 = cv.imread("Board1.png", cv.IMREAD_GRAYSCALE)
# board2 = cv.imread("Board2.png", cv.IMREAD_GRAYSCALE)
# board1 = cv.imread("../learn/opencv/images/board_golden.jpg", cv.IMREAD_GRAYSCALE)
# board2 = cv.imread("../learn/opencv/images/board_test.jpg", cv.IMREAD_GRAYSCALE)
board1 = cv.imread("../learn/opencv/images/board_golden.jpg")
board2 = cv.imread("../learn/opencv/images/board_test.jpg")

# Apply blur
board1 = cv.GaussianBlur(board1, (15,15), 0)
board2 = cv.GaussianBlur(board2, (15,15), 0)

board1 = cv.cvtColor(board1, cv.COLOR_BGR2GRAY)
board2 = cv.cvtColor(board2, cv.COLOR_BGR2GRAY)

score, diff = ssim(board1, board2, full=True)
print(f"SSIM Score: {score}")
print(type(diff))
print(diff.shape)
print(diff.dtype)

# Normalize diff image to 0–255 for applyColorMap
# b/c diff was float64 with each pixel value range [0,1], we need uint8 range [0,255] for each grayscale pixel
diff = (diff * 255).astype("uint8")
diff = 1 - diff
inferno = cv.applyColorMap(diff, cv.COLORMAP_INFERNO)

cv.imshow('difference', inferno)
if cv.waitKey(0) == ord('q'):
    cv.destroyAllWindows()

# cv.imwrite("SSIM_with_blur2_grayAfterBlur_inferno.jpg", inferno)
