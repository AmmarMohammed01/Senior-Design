# image_comparison.py (REWRITTEN)

import cv2 as cv
import numpy as np


def preprocess(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    return img


def template_score(test_roi: np.ndarray, golden_roi: np.ndarray):
    test_gray = cv.cvtColor(test_roi, cv.COLOR_BGR2GRAY)
    gold_gray = cv.cvtColor(golden_roi, cv.COLOR_BGR2GRAY)

    # test_gray = cv.resize(test_gray, (gold_gray.shape[1], gold_gray.shape[0]))

    result = cv.matchTemplate(test_gray, gold_gray, cv.TM_CCOEFF_NORMED)
    return result[0][0]


def is_missing(roi, threshold=200):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    return np.mean(gray) > threshold


def orientation_angle(roi):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None

    c = max(contours, key=cv.contourArea)
    rect = cv.minAreaRect(c)
    return rect[2]


def detect_bridge(roi):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)

    num_labels, _ = cv.connectedComponents(thresh)

    return num_labels < 2  # heuristic


def debug_bridge(roi, name="ROI"):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    
    num_labels, _ = cv.connectedComponents(thresh)
    print(f"{name} - Labels found: {num_labels}")
    
    cv.imshow(f"Threshold Debug: {name}", thresh)
    return num_labels


def get_pad_count(roi):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    # OTSU handles varying brightness better than a fixed 200
    _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    num_labels, _ = cv.connectedComponents(thresh)
    return num_labels


def classify_defect(test_roi, golden_roi, meta=None):
    score = template_score(test_roi, golden_roi)
    print("score:", score)

    # 1. If images are identical, it's "good". Period.
    if score > 0.99:
        return "good"

    if is_missing(test_roi):
        return "missing"

    # debug_bridge(test_roi)
    '''
    if detect_bridge(test_roi):
        return "solder_bridge"
    '''
    # 2. Only check for bridges if the score is lower (meaning something changed)
    # Compare Test count to Gold count
    if get_pad_count(test_roi) < get_pad_count(golden_roi):
        return "solder_bridge"

    if score < 0.5: #0.65
        if meta and "angle" in meta:
            angle_test = orientation_angle(test_roi)
            angle_gold = meta["angle"]

            if angle_test is not None and abs(angle_test - angle_gold) > 20:
                return "tombstone"

        return "misaligned"

    return "good"
