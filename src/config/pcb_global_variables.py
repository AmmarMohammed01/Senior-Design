from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
BOARDS_DIR = SCRIPT_DIR / "boards"
board_type = ""
selected_board_dir = BOARDS_DIR / board_type # not sure if this get recalculated after each time board_type is changed

LIGHTS_AVAILABLE = False
