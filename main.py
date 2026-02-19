# OpenCV Imports
import cv2 as cv
import numpy as np

# Our own .py files
from image_comparison import compare_boards
from take_image import take_golden_board_image, take_test_board_image

def main():
    """The program routine"""
    take_golden_board_image()
    take_test_board_image()
    compare_boards()

# Run program here
main()
