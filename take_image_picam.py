"""
FILE: take_image_picam.py
Contains two functions:
- take_golden_board_image(board_name)
- take_test_board_image(board_name)

NOTES: For picamera, do sudo apt install python3-picamera2. <-- this is good for pre-installed libcamera compatibility
How to connect picam ribbon-cable on Pi 5:
- shiny connector pins
    - towards usb/ethernet ports
    - towards yellow side of port
- black tape side
    - towards black/gray pull tab of port
"""

#take_image imports
import cv2 as cv
import json
from pathlib import Path

#picam imports
from picamera2 import Picamera2
from libcamera import controls
import numpy as np

height = 2592 #480
width = 4608 # 640
cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
# cam.start()

def picam_take_golden_board_image(board_dir_path):
    """Take image of GOLDEN board"""
    """Open PiCamera"""
    cam.start()
    final_frame = np.array([])

    while True:
        frame = cam.capture_array()
        cv.imshow('Capture Golden Board Image', frame)
        key = cv.waitKey(1) &0xFF # &0xFF means only the last 8 bits

        if key == ord('q'):
            final_frame = frame
            cam.close()
            cv.destroyAllWindows()
            cv.waitKey(1)
            break

    # Let user select ROI (drag a box)
    roi = cv.selectROI("Select ROI", final_frame, False) # tuple: (x,y, width, height)
    cv.destroyWindow("Select ROI")
    for i in range(4):
        cv.waitKey(1)

    # Save ROI to be used for test board capture (roi.json) file
    board_roi_file = board_dir_path / "roi.json"
    with open(board_roi_file, "w") as f:
        json.dump(roi, f)

    # Extract cropped region
    cropped_img = final_frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    golden_board_file_name = board_dir_path / "golden.png"
    print(golden_board_file_name)
    # Save and display cropped image
    cv.imwrite(golden_board_file_name, cropped_img)

def picam_take_test_board_image(board_dir_path):
    """Take image of TEST board"""

    roi = (0,0,0,0)

    # load roi data used with golden board
    board_roi_file = board_dir_path / "roi.json"
    with open(board_roi_file, "r") as f:
        roi = json.load(f)

    """Open PiCamera"""
    cam.start()
    final_frame = np.array([])

    '''Allow user to capture image by pressing q'''
    while True:
        frame = cam.capture_array()
        cv.rectangle(frame, (roi[0]-5, roi[1]-5), (roi[0]+roi[2]+5, roi[1]+roi[3]+5), (0, 255, 0), 5)
        cv.imshow('Capture Test Board Image', frame)
        key = cv.waitKey(1) &0xFF # &0xFF means only the last 8 bits

        if key == ord('q'):
            final_frame = frame
            cam.close()
            cv.destroyAllWindows()
            cv.waitKey(1)
            break

    # Extract cropped region
    cropped_img = final_frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    # Determine which # test board is this (test001, test002, test003...)
    '''
    If doesn't exist, create the file to start tracking.
    name the first file, store the number 2 in the tracker file.

    If it does exist, import the number.
    Name the file using number. Store number + 1.
    '''
    next_test_num = 1
    next_test_num_filepath = board_dir_path / "next-test-img-num.json"

    test_board_file_name = "test"

    if next_test_num_filepath.exists():
        with open(next_test_num_filepath, "r") as f:
            next_test_num = json.load(f)
            test_board_file_name = test_board_file_name + str(next_test_num) + ".png"
        with open(next_test_num_filepath, "w") as f:
            json.dump((next_test_num + 1), f)
    else:
        with open(next_test_num_filepath, "w") as f:
            test_board_file_name = test_board_file_name + str(next_test_num) + ".png"
            json.dump((next_test_num + 1), f)

    # Save and display cropped image
    test_board_filepath = board_dir_path / test_board_file_name
    cv.imwrite(test_board_filepath, cropped_img)

