# OpenCV Imports
import cv2 as cv
import numpy as np

# Our own .py files
from image_comparison import compare_boards
from take_image import take_golden_board_image, take_test_board_image
from map_errors import map_errors

def main():
    """The program routine"""

    '''
    GUI over here:
    - Select from list of existing board types
    - Add new board type
    - Remove board type
    '''

    print("What is the name of the golden board?")
    board_type = input()
    take_golden_board_image(board_type)

    # print("What type of test board is being used")
    take_test_board_image(board_type)
    # compare_boards("./images/board_golden.jpg", "./images/board_test.jpg")

# Run program here
main()

