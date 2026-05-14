from pathlib import Path
import shutil
from tkinter import Tk, filedialog

import src.config.pcb_global_variables as gv

def import_ml_model():
    # Open menu, allow user to select folder to drag and paste ML model
    # Already have code for selecting board

    """
    Opens a file explorer so the user can select a file,
    then copies it into the destination folder.
    """

    board_face = input("Select board face ('top' or 'bottom'): ")
    board_face = board_face.lower()
    selected_board_dir_with_face = gv.selected_board_dir / board_face

    # Hide tkinter root window
    root = Tk()
    root.withdraw()

    # Open file explorer
    selected_file = filedialog.askopenfilename(
        title="Select a file"
    )

    # User cancelled
    if not selected_file:
        print("No file selected.")
        return None

    source_path = Path(selected_file)
    destination_path = Path(selected_board_dir_with_face)

    # Create destination folder if needed
    destination_path.mkdir(parents=True, exist_ok=True)

    # Final copied file path
    final_path = destination_path / source_path.name

    # Copy file
    shutil.copy2(source_path, final_path)

    print(f"Uploaded file to: {final_path}")

    return final_path
