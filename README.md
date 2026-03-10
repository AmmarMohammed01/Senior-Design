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
