# orb_method.py (REWRITTEN)

import cv2 as cv
import numpy as np

def order_points(pts):
    """Order points: top-left, top-right, bottom-right, bottom-left"""
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


'''
def detect_board_corners(img: np.ndarray):
    """Detect largest rectangular contour (PCB)"""
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blur, 50, 150)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found")

    largest = max(contours, key=cv.contourArea)

    epsilon = 0.02 * cv.arcLength(largest, True)
    approx = cv.approxPolyDP(largest, epsilon, True)

    if len(approx) != 4:
        raise ValueError("Board contour is not 4-sided")

    pts = approx.reshape(4, 2)
    return order_points(pts)
'''

'''
def detect_board_corners(img, debug=True):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blur, 50, 150)

    if debug:
        cv.imshow("1 - Gray", gray)
        cv.imshow("2 - Edges", edges)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found")

    # Draw all contours
    contour_vis = img.copy()
    cv.drawContours(contour_vis, contours, -1, (0,255,0), 2)

    # Largest contour
    largest = max(contours, key=cv.contourArea)

    largest_vis = img.copy()
    cv.drawContours(largest_vis, [largest], -1, (0,0,255), 3)

    epsilon = 0.02 * cv.arcLength(largest, True)
    approx = cv.approxPolyDP(largest, epsilon, True)

    approx_vis = img.copy()
    cv.drawContours(approx_vis, [approx], -1, (255,0,0), 3)

    # Draw points
    for pt in approx:
        x, y = pt[0]
        cv.circle(approx_vis, (x, y), 8, (0,255,255), -1)

    if debug:
        cv.imshow("3 - All Contours", contour_vis)
        cv.imshow("4 - Largest Contour", largest_vis)
        cv.imshow("5 - Approximated Polygon", approx_vis)
        print(f"Number of approx points: {len(approx)}")

        cv.waitKey(0)
        cv.destroyAllWindows()

    if len(approx) != 4:
        raise ValueError(f"Board contour is not 4-sided, got {len(approx)}")

    pts = approx.reshape(4, 2)
    return pts
'''

def is_near_border(contour, img_shape, margin=50):
    """Check if contour touches near image border"""
    h, w = img_shape[:2]
    for pt in contour:
        x, y = pt[0]
        if x < margin or x > w - margin or y < margin or y > h - margin:
            return True
    return False


def detect_board_corners(img, debug=True):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv.Canny(blur, 50, 150)

    # Strengthen edges (fills gaps, merges shapes)
    kernel = np.ones((7, 7), np.uint8)
    edges = cv.dilate(edges, kernel, iterations=2)
    edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    if debug:
        cv.imshow("Edges", edges)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found")

    h, w = img.shape[:2]
    min_area = 0.3 * (h * w)  # ignore small stuff like holes

    # Filter contours
    candidates = [
        c for c in contours
        if cv.contourArea(c) > min_area and is_near_border(c, img.shape)
    ]

    if not candidates:
        raise ValueError("No board-like contour found")

    # Choose best candidate
    board_contour = max(candidates, key=cv.contourArea)

    if debug:
        vis = img.copy()
        cv.drawContours(vis, [board_contour], -1, (0, 0, 255), 3)
        cv.imshow("Board Contour", vis)

    # Approximate to polygon
    epsilon = 0.05 * cv.arcLength(board_contour, True)
    approx = cv.approxPolyDP(board_contour, epsilon, True)

    if debug:
        approx_vis = img.copy()
        cv.drawContours(approx_vis, [approx], -1, (255, 0, 0), 3)

        for pt in approx:
            x, y = pt[0]
            cv.circle(approx_vis, (x, y), 8, (0, 255, 255), -1)

        cv.imshow("Approximated Polygon", approx_vis)
        print(f"Approx points: {len(approx)}")

        cv.waitKey(0)
        cv.destroyAllWindows()

    if len(approx) != 4:
        raise ValueError(f"Board contour is not 4-sided, got {len(approx)}")

    pts = approx.reshape(4, 2)
    return order_points(pts)

def align_to_golden(test_img: np.ndarray, golden_img: np.ndarray, golden_pts) -> np.ndarray:
    """
    Align test image to golden image using 4-point transform.

    golden_pts must be manually defined ONCE from golden image.
    """
    test_pts = detect_board_corners(test_img)

    H = cv.getPerspectiveTransform(test_pts.astype(np.float32),
                                   golden_pts.astype(np.float32))

    aligned = cv.warpPerspective(
        test_img,
        H,
        (golden_img.shape[1], golden_img.shape[0])
    )

    return aligned
