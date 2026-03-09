"""
DEV:
add_board_type():
- ADD OPTION TO ESCAPE BOARD CREATION PROCESS

remove_board_type():
- MAYBE SHOW # OF CONTENTS INSIDE BEFORE DELETING

capture_golden_board_image():
- Should there be multiple golden boards?

capture_test_board_images():
- CHECK IF GOLDEN BOARD IMAGE EXISTS!!!
"""
from pathlib import Path
import shutil

# Our own .py files
from take_image import take_golden_board_image, take_test_board_image

SCRIPT_DIR = Path(__file__).parent.resolve()
BOARDS_DIR = SCRIPT_DIR / "boards"

def menu():
    print("PCB QUALITY CHECKER")
    print("1. Add new board type")
    print("2. Remove board type")
    print("3. Capture golden board image")
    print("4. Capture test board images")
    print("5. Label existing board type")
    print("6. View existing board types")
    print("q. Quit\n")

    menu_option = input("Type option number here: ")
    print()

    if menu_option == '1':
        add_board_type()
    elif menu_option == '2':
        remove_board_type()
    elif menu_option == '3':
        capture_golden_board_image()
    elif menu_option == '4':
        capture_test_board_images()
    elif menu_option == '5':
        label_board_type()
    elif menu_option == '6':
        view_board_types_option()
    elif menu_option == 'q' or menu_option == 'Q':
        print("Closing program...")
        quit()
    else:
        print("Invalid option, try again...")
        menu_return()

def add_board_type():
    print("ADD NEW BOARD TYPE")
    new_board_name = input("Name of board: ")
    print(f"Creating: '{new_board_name}'")

    try:
        new_board_dir = BOARDS_DIR / new_board_name
        new_board_dir.mkdir(parents=True, exist_ok=False)

        print(f"Board '{new_board_name}' successfully added")
        menu_return()

    except FileExistsError: # same as errno 17
        print("ERROR: That board name is already in use!")
        print("Please try again and select a different board name")
        menu_return()

def remove_board_type():
    print("REMOVE BOARD TYPE")
    print("CAUTION: Removing a board type will remove all related data!")
    print("If you need to backup the data, go to the 'boards/' folder and save the board elsewhere\n")

    view_board_types()

    remove_board_name = input("Type name of board to delete: ")

    confirm_option = input(f"Are you sure you want to remove board '{remove_board_name}'? Type y or n: ")
    if confirm_option == 'y' or confirm_option == 'Y':
        print(f"Removing board: {remove_board_name}")
        remove_board_dir = BOARDS_DIR / remove_board_name
        try:
            if remove_board_dir.exists():
                shutil.rmtree(remove_board_dir)
                print(f"Folder for '{remove_board_name}' has been deleted!")
                menu_return()
            else:
                print(f"Folder named '{remove_board_name}' does not exist.")
                menu_return()
        except Exception as err:
            print("An exception as occured", err)

    elif confirm_option == 'n' or confirm_option == 'N':
        menu_return()
    else:
        print(f"Invalid option: '{confirm_option}'.")
        menu_return()

def capture_golden_board_image():
    print("CAPTURE GOLDEN BOARD IMAGE")
    view_board_types()

    board_type = input("Select board type: ")
    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        print(f"Board type '{board_type}' was found.")

        # should see if golden board image exists?
        # should we have multiple golden boards?
        take_golden_board_image(selected_board_dir)
        print("Golden board image captured!")
        menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()


def capture_test_board_images():
    print("CAPTURE TEST BOARD IMAGES")
    view_board_types()

    board_type = input("Select board type: ")

    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        print(f"Board type '{board_type}' was found.")
        take_test_board_image(selected_board_dir)
        print("Test board image captured!")
        menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()

def label_board_type():
    print("LABEL EXISTING BOARD TYPE")
    view_board_types()

    board_type = input("Select board type: ")

def view_board_types():
    print("VIEW BOARD TYPES & BOARD INFO")

    boards_list = [board for board in BOARDS_DIR.iterdir() if board.is_dir()]
    for board in boards_list:
        print(board.name) # prints only "basename" <-- board folder name

    print()

def view_board_types_option():
    view_board_types()
    menu_return()

def menu_return():
    print("Returning to menu...\n")
    menu()

