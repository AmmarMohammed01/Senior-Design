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
from src.utils.handle_json import roi_write, roi_read
from src.processing.image_comparison import compare_boards
# from orb_method import orb_to_align
from src.processing.orb_method import align_to_golden
from src.processing.map_errors import yolo_to_rectangle
import src.hardware.ringlight_code as light

def take_golden_board_image(board_dir_path: Path, board_face: str) -> None:
    """Take image of GOLDEN board"""

    board_and_face_path = board_dir_path / board_face

    '''Open Camera'''
    board_face = board_face.lower()
    camera_index = 0 if board_face == "top" else 2 # /dev/video0 assigned to top camera, /dev/video2 assigned to bottom camera

    capture = cv.VideoCapture(camera_index)
    capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    if not capture.isOpened():
        print("Cannot open camera")
        return

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
        key = cv.waitKey(1)

        if key == ord('l'):
            light.toggle_light(board_face)
        elif key == ord('q'):
            break

    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()
    for i in range(4):
        cv.waitKey(1)

    # DEV NOTE: LET USER KNOW THEY NEED TO DRAW A RECTANGLE AROUND GOLDEN BOARD LOCATION, this will be used to crop the image and to align with test board images.
    # Let user select ROI (drag a box)
    roi = cv.selectROI("Select ROI", frame, False) # tuple: (x,y, width, height)
    cv.destroyWindow("Select ROI")
    for i in range(4):
        cv.waitKey(1)

    # Save ROI to be used for test board capture (roi.json) file
    board_roi_filepath = board_and_face_path / "roi.json"
    roi_write(board_roi_filepath, roi)
    x, y, w, h = roi

    # Extract cropped region
    cropped_img = frame[int(y):int(y+h), int(x):int(x+w)]

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
    roi = roi_read(board_roi_filepath)
    x, y, w, h = roi

    '''Open Camera'''
    board_face = board_face.lower()
    camera_index = 0 if board_face == "top" else 2 # other board_face is "bottom"

    print(f"Camera Index: {camera_index}") # DEBUG
    capture = cv.VideoCapture(camera_index)
    capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    if not capture.isOpened():
        print("Cannot open camera")
        return

    # 3. VERIFY the change
    current_w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    current_h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    print(f"Current Resolution: {int(current_w)}x{int(current_h)}")

    yolo_labels_path = board_and_face_path / "golden.txt"
    try:
        all_component_rois = yolo_to_rectangle(yolo_labels_path, h, w)
        assert all_component_rois is not None, "PCB_APP ERROR: Labels for golden board not found (golden.txt / YOLO format). You may have accidently drawn labels in PascalVOC format / golden.xml.txt. Please re-draw labels in YOLO format."
    except AssertionError as e:
        print(e) # Assert message from try block printed here
        return

    # WHILE LOOP VARIABLES
    draw_components = False
    BORDER_THICKNESS = 2 # used to be 5
    COMPONENT_BORDER_THICKNESS = 1

    '''
    WHILE LOOP
    Purpose:
    - Draw border to allow user to place board in same place as golden board.
    - Draw component borders to allow user to align individual components.

    Controls:
    - Allow user to capture image by pressing q.
    - Allow user to toggle component borders by pressing d.
    '''
    while True:
        # Capture frame-by-frame
        ret, frame = capture.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Draw border of where board is placed
        cv.rectangle(frame, (x-BORDER_THICKNESS, y-BORDER_THICKNESS), (x+w+BORDER_THICKNESS, y+h+BORDER_THICKNESS), (0, 255, 0), BORDER_THICKNESS)

        # Draw border for each component
        if draw_components:
            for i, component_roi in enumerate(all_component_rois):
                cv.rectangle(frame, (x+component_roi[1]-COMPONENT_BORDER_THICKNESS, y+component_roi[2]-COMPONENT_BORDER_THICKNESS), (x+component_roi[3]+COMPONENT_BORDER_THICKNESS, y+component_roi[4]+COMPONENT_BORDER_THICKNESS), (255, 255, 0), COMPONENT_BORDER_THICKNESS)

        cv.imshow('Capture Test Board Image', frame)

        key = cv.waitKey(1)

        if key == ord('d'):
            draw_components = not draw_components # Allow user to toggle the component boxes

        if key == ord('q'):
            if draw_components == False:
                break


    # When everything done, release the capture
    capture.release()
    cv.destroyAllWindows()
    cv.waitKey(1)

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

