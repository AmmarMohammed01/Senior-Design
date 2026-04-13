import cv2
import numpy as np
from pathlib import Path

def orb_to_align(golden_img_filename: Path, test_image_filename: Path) -> np.ndarray:
    """
    Get the golden board and test board images.
    Align the test board so that it is in the same position of the image the golden board is in.

    - Return the filepath of the "aligned" test board
    """
    '''Get the golden and test board images'''
    img1 = cv2.imread(golden_img_filename, 0)
    img2 = cv2.imread(test_image_filename, 0)

    '''Use ORB, matcher, homography to align'''
    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
    H, _ = cv2.findHomography(pts2, pts1, cv2.RANSAC)
    aligned = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]))

    '''Save the aligned test board image as aligned#.jpg'''
    print(test_image_filename)
    # print(test_image_filename[4:]) # PosixPath object is not scriptable, could use str() to convert entire path to str
    print(test_image_filename.name)
    new_test_filename = "align" + (test_image_filename.name)[4:]
    print(new_test_filename)
    # cv2.imwrite(new_test_filename, aligned)

    # return new_test_filename
    print(type(aligned))
    return aligned
