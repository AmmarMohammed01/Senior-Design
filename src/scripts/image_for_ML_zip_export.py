from pathlib import Path
import zipfile

import src.config.pcb_global_variables as gv

def create_zip_from_directory() -> Path:
    """
    Create a ZIP file containing all image files in the specified directory.

    Args:
        source_dir: Path to the folder containing images
        zip_name: Optional name for the zip file (without .zip)

    Returns:
        Path to the created ZIP file
    """

    board_face = input("Select board face ('top' or 'bottom'): ")
    board_face = board_face.lower()
    selected_board_dir_with_face = gv.selected_board_dir / board_face

    source_path = Path(selected_board_dir_with_face)

    if not source_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {selected_board_dir_with_face}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {selected_board_dir_with_face}")

    # Supported image extensions
    image_extensions = {
        ".jpg", ".jpeg", ".png", ".bmp",
        ".gif", ".tiff", ".webp"
    }

    zip_name = gv.selected_board_dir.name
    zip_path = source_path.parent / f"{zip_name}.zip"

    comparison_img_files = list(selected_board_dir_with_face.glob("compare*.jpg"))

    # Find image files
    image_files = [
        file for file in source_path.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    ]

    if not image_files:
        raise ValueError("No image files found in directory")

    # Create zip file
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for image_file in image_files:
            zipf.write(image_file, arcname=image_file.name)

    print(f"ZIP created: {zip_path}")
    print(f"Added {len(image_files)} image(s)")

    return zip_path


