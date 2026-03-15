# OpenCV Imports
import cv2 as cv
import numpy as np

# Our own .py files
from image_comparison import compare_boards
from map_errors import map_errors
from menu import menu
import select_camera

def main():
    """The program routine"""
    '''Select Camera: USB or Pi'''
    print(f"Current Choice: {select_camera.camera_choice}")
    select_camera.camera_choice = input("Which camera are you using (usb or picam): ")
    print(f"You chose: {select_camera.camera_choice}\n")

    menu()

# Run program here
main()

