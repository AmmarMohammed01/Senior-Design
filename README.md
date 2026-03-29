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

## Create venv for labelImg
### Background
labelImg is the labeling program used the label the golden boards.
A caveat we face using it is that it need to run on Python 3.9 for stability.
Hence, we need to create a Python 3.9 Virtual Environment (venv)

### Mac Instructions
1. Install Python 3.9
```bash
# Install using Homebrew
brew install python@3.9

# To check if installed
which python3.9 # should be /opt/homebrew/bin/python3.9
```

2. Create virtual environment w/ Python 3.9
```bash
python3.9 -m venv labelimg_env
```

3. Install labelImg program
```bash
source labelimg_env/bin/activate
pip install labelImg

deactivate
```

### Raspberry Pi 5 Instructions

1. Install dependencies to compile from source
```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
2. Install pyenv
```bash
curl https://pyenv.run | bash

# After installed, add this to ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Next time terminal is launched you should see something like this: 
which pyenv # /home/team2299/.pyenv/bin/pyenv
```

3. Install Python 3.9 using pyenv
```bash
pyenv install 3.9.21
```

4. Create virtual environment with Python 3.9
```bash
~/.pyenv/versions/3.9.21/bin/python -m venv labelimg_env
```

5. Install labelImg program
```bash
source labelimg_env/bin/activate
pip install labelImg

deactivate
```

6. Facing PyQt Issues
```text
I have Raspberry Pi 5. 
I have a Python program running Python 3.13.5. 
Need to launch labelImg from it. 
But labelImg need python 3.9 to run without crashing. 
I have pyenv installed. 
I ran into issue with PyQt installation when "pip install labelImg"
```

```bash
sudo apt update
sudo apt install python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools
pip install labelImg --no-deps
```

## File Structure
### Main Files in GitHub Repo
```text
.
├── README.md
├── requirements.txt: required python libraries
├── main.py
├── menu.py
├── select_camera.py
├── take_image.py
├── take_image_picam.py
├── launch_image_labeler.py
├── image_comparison.py
└── map_errors.py
```

### Python Program Descriptions
```
main.py:
- entry point of program

menu.py:
- user interface and options

select_camera.py:
- allow user to select usb or picam

take_image.py:
- capture golden and test board images

take_image_picam.py:
- capture golden and test board images with picamera

launch_image_labeler.py:
- launches labelImg to allow user to label golden board

image_comparison.py:
- compares golden board and test boards images

map_errors.py:
- map regions onto golden board found to be different,
- determine which are likely errors,
- suggest possible error types
```

### Boards would appear in a folder like this
*Note: image save type for program is .jpg*
```text
.
├── boards
│   ├── arduino
│   │   ├── golden.jpg
│   │   └── roi.json
│   ├── power
│   │   ├── classes.txt
│   │   ├── golden.jpg
│   │   ├── golden.txt
│   │   └── roi.json
│   ├── buck
│   │   ├── classes.txt
│   │   ├── golden.jpg
│   │   ├── golden.txt
│   │   ├── next-test-img-num.json
│   │   ├── roi.json
│   │   ├── test1.jpg
│   │   ├── test2.jpg
│   │   ├── test23.jpg
│   │   ├── test24.jpg
│   │   ├── test25.jpg
│   │   ├── test26.jpg
│   │   ├── test27.jpg
│   │   ├── test28.jpg
│   │   ├── test29.jpg
│   │   └── test30.jpg
│   └── buck-boost
│       ├── golden.jpg
│       ├── next-test-img-num.json
│       ├── roi.json
│       ├── test1.jpg
│       └── test2.jpg
```

### Images currently included in GitHub repository
```text
├── images
│   ├── board_golden.jpg
│   ├── board_golden.txt
│   ├── board_inferno.jpg
│   ├── board_test.jpg
│   ├── classes.txt
│   ├── golden.png
└   └── test1.png
```
