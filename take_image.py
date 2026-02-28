"""
FILE: take_image.py
Contains two functions:
- take_golden_board_image(board_name)
- take_test_board_image(board_name)
"""

'''
TODO: FIX ROI variable, before dividing the code in functions I used the roi from take_golden_board for take_test_board
'''

import cv2 as cv

def take_golden_board_image(board_name):
    """Take image of GOLDEN board"""
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

    golden_board_file_name = board_name + "-golden.png"
    # Save and display cropped image
    cv.imwrite(golden_board_file_name, cropped_img)
    # MAYBE RETURN ROI for test board image, NEED TO STORE SINCE TAKING MULTIPLE TEST BOARD IMAGES

def take_test_board_image(board_name):
    """Take image of TEST board"""

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
    test_board_file_name = board_name + "-test.png"
    cv.imwrite(test_board_file_name, cropped_img)

    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()
