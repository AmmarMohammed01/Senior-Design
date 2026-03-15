'''
FILE: launch_image_labeler.py
This file will be used to launch the labelImg application after being prompted in a menu option.
This application will be used to allow user to label the golden board image.
'''

'''DEV NOTE: Add a way to pass a golden board file name to open up the image file on launch'''
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
# venv_python = r"C:\path\to\your\venv39\Scripts\labelImg.exe" # Windows system
labelImg_path = SCRIPT_DIR / ".python3.9venv/bin/labelImg" # Assumes UNIX-like system

try:
    # Call the executable
    subprocess.run([labelImg_path], check=True)
except FileNotFoundError:
    print(f"Error: Could not find labelImg at {labelImg_path}")
except subprocess.CalledProcessError as e:
    print(f"Error launching labelImg: {e}")
