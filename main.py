# Our own .py files
from map_errors import map_errors
# from menu import menu
from menu import menu_board_manager
import select_camera

def main():
    """The program routine"""
    '''Select Camera: USB or Pi'''
    print(f"Current Choice: {select_camera.camera_choice}")
    select_camera.camera_choice = input("Which camera are you using (usb or picam): ")
    print(f"You chose: {select_camera.camera_choice}\n")

    # menu()
    menu_board_manager()

# Run program here
main()

