import os
import shutil

def menu():
    print("PCB QUALITY CHECKER")
    print("1. Add new board type")
    print("2. Label existing board type")
    print("3. Add test board images")
    print("4. View existing board types")
    print("5. Remove board type")
    print("q. Quit\n")

    menu_option = input("Type option number here: ")
    print()

    if menu_option == '1':
        add_board_type()
    elif menu_option == '2':
        label_board_type()
    elif menu_option == '3':
        add_test_board_images()
    elif menu_option == '4':
        view_board_types()
    elif menu_option == '5':
        remove_board_type()
    elif menu_option == 'q' or menu_option == 'Q':
        print("Closing program...")
        quit()

def add_board_type():
    print("ADD NEW BOARD TYPE")
    new_board_name = input("Name of board: ")
    print(f"Creating: '{new_board_name}'")

    try:
        os.makedirs(f"./boards/{new_board_name}")
        print(f"Board '{new_board_name}' successfully added")
        menu_return()

    except FileExistsError:
        print("That board name is already in use!")
        print("Please try again and select a different board name")
        menu_return()

def remove_board_type():
    print("REMOVE BOARD TYPE")
    print("CAUTION: Removing a board type will remove all related data!")
    print("If you need to backup the data, go to the 'boards/' folder and save the board elsewhere\n")
    remove_board_name = input("Type name of board to delete: ")

    confirm_option = input(f"Are you sure you want to remove board '{remove_board_name}'? Type y or n: ")
    if confirm_option == 'y' or confirm_option == 'Y':
        print(f"Removing board: {remove_board_name}")
        try:
            if os.path.exists(f"./boards/{remove_board_name}"):
                shutil.rmtree(f"./boards/{remove_board_name}")
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

def label_board_type():
    print()

def add_test_board_images():
    print()

def view_board_types():
    print()

def menu_return():
    print("Returning to menu...\n")
    menu()

menu()
