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


def classify_defect(test_roi, golden_roi, meta=None):
    score = template_score(test_roi, golden_roi)
    print("score:", score)

    if is_missing(test_roi):
        return "missing"

    if score < 0.5: #0.65
        if meta and "angle" in meta:
            angle_test = orientation_angle(test_roi)
            angle_gold = meta["angle"]

            if angle_test is not None and abs(angle_test - angle_gold) > 20:
                return "tombstone"

        return "misaligned"

    '''
    if detect_bridge(test_roi):
        return "solder_bridge"
    '''

    return "good"
