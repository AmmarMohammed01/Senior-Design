from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
BOARDS_DIR = PROJECT_DIR / "boards"
board_type = ""
selected_board_dir = BOARDS_DIR / board_type # not sure if this get recalculated after each time board_type is changed

LIGHTS_AVAILABLE = False

'''
for p in Path(__file__).resolve().parents:
    print(p)
'''
