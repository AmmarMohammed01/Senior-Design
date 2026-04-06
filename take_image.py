"""
FILE: take_image.py
Contains two functions:
- take_golden_board_image(board_name)
- take_test_board_image(board_name)
"""

import cv2 as cv
import json
from pathlib import Path

# our own .py files
from image_comparison import compare_boards
from orb_method import orb_to_align

def take_golden_board_image(board_dir_path):
    """Take image of GOLDEN board"""
    '''Open Camera'''
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    '''Allow user to capture image by pressing q'''
    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv.imshow('Capture Golden Board Image', frame)
        if cv.waitKey(1) == ord('q'):
            # When everything done, release the capture
            capture.release()
            cv.destroyAllWindows()
            for i in range(4):
                cv.waitKey(1)
            break

    # DEV NOTE: LET USER KNOW THEY NEED TO DRAW A RECTANGLE AROUND GOLDEN BOARD LOCATION, this will be used to crop the image and to align with test board images.
    # Let user select ROI (drag a box)
    roi = cv.selectROI("Select ROI", frame, False) # tuple: (x,y, width, height)
    cv.destroyWindow("Select ROI")
    for i in range(4):
        cv.waitKey(1)

    # Save ROI to be used for test board capture (roi.json) file
    board_roi_file = board_dir_path / "roi.json"
    with open(board_roi_file, "w") as f:
        json.dump(roi, f)

    # Extract cropped region
    cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    golden_board_file_name = board_dir_path / "golden.jpg"
    print(golden_board_file_name)
    # Save and display cropped image
    cv.imwrite(golden_board_file_name, cropped_img)

def take_test_board_image(board_dir_path):
    """Take image of TEST board"""

    roi = (0,0,0,0)
    # load roi data used with golden board
    board_roi_file = board_dir_path / "roi.json"
    with open(board_roi_file, "r") as f:
        roi = json.load(f)

    '''Open Camera'''
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    '''Allow user to capture image by pressing q'''
    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv.rectangle(frame, (roi[0]-5, roi[1]-5), (roi[0]+roi[2]+5, roi[1]+roi[3]+5), (0, 255, 0), 5)

        cv.imshow('Capture Test Board Image', frame)
        if cv.waitKey(1) == ord('q'):
            # When everything done, release the capture
            capture.release()
            cv.destroyAllWindows()
            cv.waitKey(1)
            break

    # Extract cropped region
    cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

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
    comparison_result_file_name = "compare"

    if next_test_num_filepath.exists():
        with open(next_test_num_filepath, "r") as f:
            next_test_num = json.load(f)
            test_board_file_name = test_board_file_name + str(next_test_num) + ".jpg"
            comparison_result_file_name = comparison_result_file_name + str(next_test_num) + ".jpg"
        with open(next_test_num_filepath, "w") as f:
            json.dump((next_test_num + 1), f)
    else:
        with open(next_test_num_filepath, "w") as f:
            test_board_file_name = test_board_file_name + str(next_test_num) + ".jpg"
            comparison_result_file_name = comparison_result_file_name + str(next_test_num) + ".jpg"
            json.dump((next_test_num + 1), f)

    # Save and display cropped image
    test_board_filepath = board_dir_path / test_board_file_name
    cv.imwrite(test_board_filepath, cropped_img)
    print(f"Saved test board image as {test_board_file_name} in {board_dir_path}")

    '''CONVERT TEST IMAGE TO ALIGNED IMAGE IN RELATION TO GOLDEN BOARD'''
    golden_board_filepath = board_dir_path / "golden.jpg"
    align_board_filepath = orb_to_align(golden_board_filepath, test_board_filepath)

    '''RUN IMAGE COMPARISON'''
    comparison_result_filepath = board_dir_path / comparison_result_file_name
    compare_boards(golden_board_filepath, align_board_filepath, comparison_result_filepath)

