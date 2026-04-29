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
# from orb_method import orb_to_align
from orb_method import align_to_golden
from map_errors import yolo_to_rectangle

def take_golden_board_image(board_dir_path: Path, board_face: str) -> None:
    """Take image of GOLDEN board"""

    board_and_face_path = board_dir_path / board_face

    '''Open Camera'''
    board_face = board_face.lower()
    camera_index = 0 if board_face == "top" else 1 # other board_face is "bottom"

    capture = cv.VideoCapture(camera_index)
    capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    # 3. VERIFY the change
    current_w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    current_h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    print(f"Current Resolution: {int(current_w)}x{int(current_h)}")

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
    board_roi_filepath = board_and_face_path / "roi.json"
    with open(board_roi_filepath, "w") as f:
        json.dump(roi, f)

    # Extract cropped region
    cropped_img = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    golden_board_filepath = board_and_face_path / "golden.jpg"
    print(golden_board_filepath)
    # Save and display cropped image
    cv.imwrite(golden_board_filepath, cropped_img)

def take_test_board_image(board_dir_path: Path, board_face: str) -> None:
    """Take image of TEST board"""

    board_and_face_path = board_dir_path / board_face

    roi = (0,0,0,0)
    # load roi data used with golden board
    board_roi_filepath = board_and_face_path / "roi.json"
    with open(board_roi_filepath, "r") as f:
        roi = json.load(f)

    '''Open Camera'''
    board_face = board_face.lower()
    camera_index = 0 if board_face == "top" else 1 # other board_face is "bottom"

    capture = cv.VideoCapture(camera_index)
    capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    # 3. VERIFY the change
    current_w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    current_h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    print(f"Current Resolution: {int(current_w)}x{int(current_h)}")

    yolo_labels_path = board_and_face_path / "golden.txt"
    all_component_rois = yolo_to_rectangle(yolo_labels_path, current_h, current_w)

    '''Allow user to capture image by pressing q'''
    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # cv.rectangle(frame, (roi[0]-5, roi[1]-5), (roi[0]+roi[2]+5, roi[1]+roi[3]+5), (0, 255, 0), 5)
        border_thickness = 2 # used to be 5
        cv.rectangle(frame, (roi[0]-border_thickness, roi[1]-border_thickness), (roi[0]+roi[2]+border_thickness, roi[1]+roi[3]+border_thickness), (0, 255, 0), border_thickness)

        for i, component_roi in enumerate(all_component_rois):
            cv.rectangle(frame, (component_roi[1]-border_thickness, component_roi[2]-border_thickness), (component_roi[3]+border_thickness, component_roi[4]+border_thickness), (255, 255, 0), border_thickness)

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
    next_test_num_filepath = board_and_face_path / "next-test-img-num.json"

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
    test_board_filepath = board_and_face_path / test_board_file_name
    cv.imwrite(test_board_filepath, cropped_img)
    print(f"Saved test board image as {test_board_file_name} in {board_dir_path}")

    '''CONVERT TEST IMAGE TO ALIGNED IMAGE IN RELATION TO GOLDEN BOARD'''
    golden_board_filepath = board_and_face_path / "golden.jpg"
    # aligned_board_img = orb_to_align(golden_board_filepath, test_board_filepath)
    golden_board_image = cv.imread(golden_board_filepath)
    # aligned_board_img = align_to_golden(test_img=cropped_img, golden_img=golden_board_image, golden_pts=)
    aligned_board_img = None


    # aligned_board_filepath = board_and_face_path / aligned_board_file_name
    # cv.imwrite(aligned_board_filepath, aligned_board_img)

    '''RUN IMAGE COMPARISON'''
    comparison_result_filepath = board_and_face_path / comparison_result_file_name
    # compare_boards(golden_board_filepath, aligned_board_filepath, comparison_result_filepath)
    compare_boards(golden_board_filepath, test_board_filepath, comparison_result_filepath)

