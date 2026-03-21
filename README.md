# Senior-Design
## How to run code?
### First time install python libraries (setting up Python Virtual Enivronment):
1. Open the folder
2. In terminal run the following for installing libraries on Mac/Linux:
```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
or installing libraries on Raspberry Pi:
```bash
# Raspberry Pi
sudo apt install python3-picamera2
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Now you can run the program:
```bash
python main.py
```
4. After finished running program, to close the Python Virtual Environment type in terminal
```bash
deactivate
```

### Running code with python libraries already installed:
1. Open the folder
2. In terminal run:
```bash
source .venv/bin/activate
```
3. Now you can run the program:
```bash
python main.py
```
4. After finished running program, to close the Python Virtual Environment type in terminal
```bash
deactivate
```

## File Structure
```text
.
├── README.md
├── requirements.txt: required python libraries
├── main.py: entry point of program
├── menu.py: user interface and options
├── select_camera.py: allow user to select usb or picam
├── take_image.py: capture golden and test board images
├── take_image_picam.py: capture golden and test board images with picamera
├── launch_image_labeler.py: launches labelImg to allow user to label golden board
├── image_comparison.py: compares golden board and test boards images
└── map_errors.py: map regions onto golden board found to be different, determine which are likely errors, suggest possible error types
```

### Boards would appear in a folder like this
```text
.
├── boards
│   ├── arduino
│   │   ├── golden.png
│   │   └── roi.json
│   ├── power
│   │   ├── classes.txt
│   │   ├── golden.png
│   │   ├── golden.txt
│   │   └── roi.json
│   ├── buck
│   │   ├── classes.txt
│   │   ├── golden.png
│   │   ├── golden.txt
│   │   ├── next-test-img-num.json
│   │   ├── roi.json
│   │   ├── test1.png
│   │   ├── test2.png
│   │   ├── test23.png
│   │   ├── test24.png
│   │   ├── test25.png
│   │   ├── test26.png
│   │   ├── test27.png
│   │   ├── test28.png
│   │   ├── test29.png
│   │   └── test30.png
│   └── buck-boost
│       ├── golden.png
│       ├── next-test-img-num.json
│       ├── roi.json
│       ├── test1.png
│       └── test2.png
```

### Images currently included in GitHub repository
```text
├── images
│   ├── board_golden.jpg
│   ├── board_golden.txt
│   ├── board_inferno.jpg
│   ├── board_test.jpg
│   └── classes.txt
```
