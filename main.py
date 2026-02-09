import cv2 as cv
import numpy as np

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
# Extract cropped region
cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

# Save and display cropped image
cv.imwrite("Cropped.png", cropped_img)
cv.imshow("Cropped Image", cropped_img)
cv.waitKey(0)
cv.destroyAllWindows()
'''
