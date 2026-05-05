import json

def roi_read(roi_path):
    with open(roi_path, "r") as f:
        roi = json.load(f)
        return roi

def roi_write(roi_path, roi):
    with open(roi_path, "w") as f:
        json.dump(roi, f)
