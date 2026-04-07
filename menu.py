"""
DEV NOTES:
add_board_type():
- ADD OPTION TO ESCAPE BOARD CREATION PROCESS

remove_board_type():
- MAYBE SHOW # OF CONTENTS INSIDE BEFORE DELETING

capture_golden_board_image():
- Should there be multiple golden boards?

capture_test_board_images():
- CHECK IF GOLDEN BOARD IMAGE EXISTS!!!
"""
# File management libraries
from pathlib import Path
import shutil

# Our own .py files
from take_image import take_golden_board_image, take_test_board_image
from take_image_picam import picam_take_golden_board_image, picam_take_test_board_image
import select_camera
from launch_image_labeler import launch_image_labeler
from image_comparison import compare_boards
from map_errors import generate_defect_frequency_map, map_errors

SCRIPT_DIR = Path(__file__).parent.resolve()
BOARDS_DIR = SCRIPT_DIR / "boards"

def menu():
    while True:
        print(select_camera.camera_choice)
        print("PCB QUALITY CHECKER")
        print("-------------------")
        print("1. Add new board type")
        print("2. Remove board type")
        print("3. Capture golden board image")
        print("4. Capture test board images")
        print("5. Label existing board type")
        print("6. View existing board types")
        print("7. Compare golden and test board images")
        print("8. Generate defect frequency map")
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
        elif menu_option == '7':
            run_comparison_board_type()
        elif menu_option == '8':
            option_defect_frequency_map()
        elif menu_option == 'q' or menu_option == 'Q':
            print("Closing program...")
            break
        else:
            print("Invalid option, try again...")
            menu_return()

def add_board_type() -> None:
    """Creates a new folder to store images of a specified board type."""
    print("ADD NEW BOARD TYPE")
    print("------------------")
    new_board_name = input("Name of board: ")

    try:
        new_board_dir = BOARDS_DIR / new_board_name
        new_board_dir.mkdir(parents=True, exist_ok=False)

        print(f"SUCCESS: Board '{new_board_name}' folder created.")
        menu_return()

    except FileExistsError: # same as errno 17
        print(f"ERROR: The board name, {new_board_name}, is already in use!")
        print("Please try again and select a different board name")
        menu_return()

def remove_board_type() -> None:
    """Deletes a folder of a board type, including all images and data within."""
    print("REMOVE BOARD TYPE")
    print("-----------------")
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
    """First: user to select a board type.
    Next: Camera window opens.
    Then: User presses 'Q' to capture an image of 'golden'/perfect board.
    Finally: User selects rectangular region around the board - by click and dragging - then presses space to confirm."""

    print("CAPTURE GOLDEN BOARD IMAGE")
    print("--------------------------")

    view_board_types()
    board_type = input("Select board type: ")
    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        print(f"Board type '{board_type}' was found.")

        # should see if golden board image exists?
        # should we have multiple golden boards?
        if select_camera.camera_choice == "usb":
            take_golden_board_image(selected_board_dir, "top")
            take_golden_board_image(selected_board_dir, "bottom")
        elif select_camera.camera_choice == "picam":
            picam_take_golden_board_image(selected_board_dir)

        print("Golden board image captured!")
        menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()


def capture_test_board_images():
    """First: user to select a board type.
    Next: Camera window opens. It loads the rectangular outline user created when capturing golden board to help align test boards.
    Then: User presses 'Q' to capture an image of test board.
    Finally: Alignment and comparison are run on the test image immediately after."""

    print("CAPTURE TEST BOARD IMAGES")
    print("-------------------------")

    view_board_types()
    board_type = input("Select board type: ")
    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        print(f"Board type '{board_type}' was found.")

        '''Check if golden board image exists, more specifically if roi coordinates of golden board exist''' 
        roi_filepath = selected_board_dir / "roi.json"

        if roi_filepath.exists():
            if select_camera.camera_choice == "usb":
                take_test_board_image(selected_board_dir, "top")
                take_test_board_image(selected_board_dir, "bottom")
                print("Test board image captured!")
            elif select_camera.camera_choice == "picam":
                picam_take_test_board_image(selected_board_dir)
                print("Test board image captured!")
            menu_return()
        else:
            print("ERROR: Golden board image not found") # Specifically ROI.json was not found
            menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()

def label_board_type():
    """First: User selects board type.
    Next: labelImg program launches.
    Then: User can label components and save labels in YOLO format.
    Finally: User saves, exits, and returns to this program.
    """
    print("LABEL EXISTING BOARD TYPE")
    print("-------------------------")
    view_board_types()
    print("NOTE: When the program launches, the save format will show \"YOLO\" but is actually PascalVOC.")
    print("NOTE continued: This will save labels as .xml.txt instead of .txt")
    print("ACTION: User must re-toggle the save format until it lands on \"YOLO\" again.\n")

    print("INSTRUCTIONS:")
    print("After selecting a board type, labelImg program will open.")
    print("This will be used to label golden board components.")
    print("Click 'Create Rectangle Box' and drag and select the region around component of choice.")
    print("Then give the rectangle region a name related to the component.")
    print("Once finished labeling all the components, click save and the file should automatically be named \"golden.txt\"")

    board_type = input("Select board type: ")
    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        golden_board_file = selected_board_dir / "golden.jpg"
        print(f"Board type '{board_type}' was found.")
        print(golden_board_file)
        launch_image_labeler(golden_board_file)

        menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()

def view_board_types():
    """This function is used in multiple menu options to give the user
    a sense of what boards already exist in the file system before the
    user removes, captures a golden or test board, or labels a board."""
    print("VIEW BOARD TYPES & BOARD INFO")
    print("-----------------------------")

    boards_list = [board for board in BOARDS_DIR.iterdir() if board.is_dir()]
    for board in boards_list:
        print(board.name) # prints only "basename" <-- board folder name

    print()

def view_board_types_option():
    """This is the actual (standalone) menu option that allows the user to see the existing board types"""
    view_board_types()
    menu_return()

def run_comparison_board_type():
    """This is the menu option for running a board comparison for a board type.
    The program will look at the golden board for a selected board type and compare it to the test boards captured for the same board type."""
    print("RUN COMPARISON ON A BOARD TYPE")
    print("------------------------------")

    view_board_types()
    board_type = input("Select a board type: ")
    selected_board_dir = BOARDS_DIR / board_type

    # Check if board type exists, else return to menu
    if selected_board_dir.exists():
        print(f"Board type '{board_type}' was found.")

        '''CODING PLAN:'''
        '''Get golden board image'''
        golden_board_filepath = selected_board_dir / "golden.jpg"

        '''Get test board images''' # NOTE: we have multiple test boards. How to store each difference image result? I think best action is to create a frequency map.
        input_test_board_filename = input("Type the filename of the test board you want to compare golden board to (example: test1.jpg): ")
        test_board_filepath = selected_board_dir / input_test_board_filename

        '''Compare golden board to each test board'''
        compare_boards(golden_board_filepath, test_board_filepath)

        '''Maybe make a frequency map of where the most errors occur'''

        menu_return()
    else:
        print(f"ERROR: The board '{board_type}' was not found!")
        menu_return()


def option_defect_frequency_map():
    """This menu option will generate a frequency map displaying the number of times each component was detected for having a potential defect,
    which will then be overlayed onto the golden board."""
    print("GENERATE DEFECT FREQUENCY MAP")
    print("-----------------------------")

    view_board_types()
    board_type = input("Select a board type: ")
    selected_board_dir = BOARDS_DIR / board_type
    golden_board_filepath = selected_board_dir / "golden.jpg"
    next_test_img_filepath = selected_board_dir / "next-test-img-num.json"
    yolo_coordinates_filepath = selected_board_dir / "golden.txt"
    yolo_classes_filepath = selected_board_dir / "classes.txt"

    # Check if board type exists
    if not selected_board_dir.exists():
        print(f"ERROR: The board '{board_type}' was not found!")
        return menu_return() # NOTE TO SELF: same as return None, so you could have menu_return followed by return if wanted, or on same line

    # Check if golden board image exists
    elif not golden_board_filepath.exists():
        print(f"ERROR: The golden board image for '{board_type}' was not found!")
        print("Please capture image of golden board first.")
        return menu_return()

    # Check if board type has test images
    elif not next_test_img_filepath.exists():
        print(f"ERROR: No test images for '{board_type}' were found!'")
        print("Please capture image of a test board first.")
        return menu_return()

    # Check if the board labels exists
    elif not yolo_coordinates_filepath.exists() or not yolo_classes_filepath.exists():
        print(f"ERROR: No labels for '{board_type} were found!'")
        print("Please label the golden board image first.")
        return menu_return()

    # Generate the frequency map if all above conditions are met
    print(f"Board type '{board_type}' was found.")

    generate_defect_frequency_map(yolo_coordinates_filepath=yolo_coordinates_filepath, selected_board_dir=selected_board_dir, golden_board_filepath=golden_board_filepath, yolo_classes_filepath=yolo_classes_filepath)


    return menu_return()

def menu_return():
    print("Returning to menu...\n")

