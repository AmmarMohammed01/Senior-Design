# Our own .py files
from src.ui.menu import menu_board_manager
import src.config.select_camera as select_camera

if __name__ == "__main__":
    '''Select Camera: USB or Pi'''
    print(f"Current Choice: {select_camera.camera_choice}")
    select_camera.camera_choice = input("Which camera are you using (usb or picam): ")
    print(f"You chose: {select_camera.camera_choice}\n")

    # menu()
    menu_board_manager()
