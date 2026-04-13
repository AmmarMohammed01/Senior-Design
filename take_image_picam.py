"""
FILE: take_image_picam.py
Contains two functions:
- picam_take_golden_board_image(board_name)
- picam_take_test_board_image(board_name)

NOTES: For picamera, do sudo apt install python3-picamera2. <-- this is good for pre-installed libcamera compatibility
python3 -m venv --system-site-packages .venv
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

# our own .py files
from image_comparison import compare_boards

#picam imports
try:
    '''Import picamera only if the picamera library is installed on user's device'''
    from picamera2 import Picamera2
    from libcamera import controls
    HAS_PICAMERA = True

    '''
    height = 2592 #480
    width = 4608 # 640
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    '''
    # cam.start()
except (ImportError, ModuleNotFoundError):
    HAS_PICAMERA = False
    print("Picamera not found. Please use USB webcam instead.")
import numpy as np

def picam_take_golden_board_image(board_dir_path: Path, board_face: str) -> None:
    """Take image of GOLDEN board"""
    """Open PiCamera"""
    height = 2592 #480
    width = 4608 # 640

    if board_face == "top":
        cam = Picamera2(0) # Port 0: near ethernet port
    elif board_face == "bottom":
        cam = Picamera2(1) # Port 1: near MicroHDMI port
    else:
        cam = Picamera2(0)

    cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
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
    board_roi_file = board_dir_path / board_face / "roi.json"
    with open(board_roi_file, "w") as f:
        json.dump(roi, f)

    # Extract cropped region
    cropped_img = final_frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    golden_board_file_name = board_dir_path / board_face / "golden.jpg"
    print(golden_board_file_name)
    # Save and display cropped image
    cv.imwrite(golden_board_file_name, cropped_img)

def picam_take_test_board_image(board_dir_path: Path, board_face: str) -> None:
    """Take image of TEST board"""

    roi = (0,0,0,0)

    # load roi data used with golden board
    board_roi_file = board_dir_path / board_face / "roi.json"
    with open(board_roi_file, "r") as f:
        roi = json.load(f)

    """Open PiCamera"""
    height = 2592 #480
    width = 4608 # 640

    if board_face == "top":
        cam = Picamera2(0) # Port 0: near ethernet port
    elif board_face == "bottom":
        cam = Picamera2(1) # Port 1: near MicroHDMI port
    else:
        cam = Picamera2(0)

    cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
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
    next_test_num_filepath = board_dir_path / board_face / "next-test-img-num.json"

    test_board_file_name = "test"
    comparison_result_file_name = "compare"
    aligned_board_file_name = "align"

    if next_test_num_filepath.exists():
        with open(next_test_num_filepath, "r") as f:
            next_test_num = json.load(f)
            test_board_file_name = test_board_file_name + str(next_test_num) + ".jpg"
            comparison_result_file_name = comparison_result_file_name + str(next_test_num) + ".jpg"
            aligned_board_file_name = aligned_board_file_name + str(next_test_num) + ".jpg"
        with open(next_test_num_filepath, "w") as f:
            json.dump((next_test_num + 1), f)
    else:
        with open(next_test_num_filepath, "w") as f:
            test_board_file_name = test_board_file_name + str(next_test_num) + ".jpg"
            comparison_result_file_name = comparison_result_file_name + str(next_test_num) + ".jpg"
            aligned_board_file_name = aligned_board_file_name + str(next_test_num) + ".jpg"
            json.dump((next_test_num + 1), f)

    # Save and display cropped image
    test_board_filepath = board_dir_path / board_face / test_board_file_name
    cv.imwrite(test_board_filepath, cropped_img)
    print(f"Saved test board image as {test_board_file_name} in {board_dir_path}")

    '''CONVERT TEST IMAGE TO ALIGNED IMAGE IN RELATION TO GOLDEN BOARD'''
    golden_board_filepath = board_dir_path / "golden.jpg"
    aligned_board_img = orb_to_align(golden_board_filepath, test_board_filepath)
    aligned_board_filepath = board_dir_path / board_face / aligned_board_file_name
    cv.imwrite(aligned_board_filepath, aligned_board_img)

    '''RUN IMAGE COMPARISON'''
    comparison_result_filepath = board_dir_path / board_face / comparison_result_file_name
    compare_boards(golden_board_filepath, aligned_board_filepath, comparison_result_filepath)

