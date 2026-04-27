# map_errors.py (REWRITTEN)

import cv2 as cv
import numpy as np
from orb_method import align_to_golden
from image_comparison import classify_defect


class YOLOLabel:
    def __init__(self):
        self.label_name = ""
        self.label_x = 0.0
        self.label_y = 0.0
        self.label_width = 0.0
        self.label_height = 0.0

    def convert_to_label(self, label_coordinates, label_classes):
        parts = label_coordinates.split()
        self.label_name = label_classes[int(parts[0])]
        self.label_x = float(parts[1])
        self.label_y = float(parts[2])
        self.label_width = float(parts[3])
        self.label_height = float(parts[4])


def get_YOLO_label(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]


def get_YOLO_classes(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]


def extract_roi(img, label):
    h, w = img.shape[:2]

    cx = label.label_x * w
    cy = label.label_y * h
    bw = label.label_width * w
    bh = label.label_height * h

    x1 = int(cx - bw / 2)
    y1 = int(cy - bh / 2)
    x2 = int(cx + bw / 2)
    y2 = int(cy + bh / 2)

    pad = 5
    return img[max(0,y1-pad):y2+pad, max(0,x1-pad):x2+pad]


def build_golden_library(golden_img, labels, class_names):
    library = {}

    for label_info in labels:
        lbl = YOLOLabel()
        lbl.convert_to_label(label_info, class_names)

        roi = extract_roi(golden_img, lbl)
        library[lbl.label_name] = roi

    return library


def map_errors(test_img_path,
               golden_img_path,
               yolo_labels_path,
               yolo_classes_path,
               golden_pts):
    
    golden_img = cv.imread(golden_img_path)
    test_img = cv.imread(test_img_path)

    assert golden_img is not None
    assert test_img is not None

    # ALIGN
    # aligned = align_to_golden(test_img, golden_img, golden_pts)

    labels = get_YOLO_label(yolo_labels_path)
    class_names = get_YOLO_classes(yolo_classes_path)

    golden_lib = build_golden_library(golden_img, labels, class_names)

    output = golden_img.copy()

    for label_info in labels:
        lbl = YOLOLabel()
        lbl.convert_to_label(label_info, class_names)

        # test_roi = extract_roi(aligned, lbl)
        test_roi = extract_roi(test_img, lbl)
        golden_roi = golden_lib[lbl.label_name]

        defect = classify_defect(test_roi, golden_roi)

        h, w = golden_img.shape[:2]
        cx = int(lbl.label_x * w)
        cy = int(lbl.label_y * h)

        color = (0,255,0) if defect == "good" else (0,0,255)

        cv.putText(output, defect, (cx, cy),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv.imshow("Result", output)

    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
