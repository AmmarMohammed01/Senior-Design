"""
FILE: image_comparison.py

PURPOSE:
- Compare golden board and test board images,
- create an image showing the differences thru SSIM,
- Apply inferno filter to differences image

Contains two functions:
- ssim(img1, img2, window_size=11, K1=0.01, K2=0.03, L=255)
- compare_boards()
"""

import cv2 as cv
import numpy as np

# --- Pure-Python SSIM implementation ---
def ssim(img1, img2, window_size=11, K1=0.01, K2=0.03, L=255):
    """
    Compute the Structural Similarity Index (SSIM) between two grayscale images.
    Pure Python + NumPy + OpenCV, no C extensions.
    
    Returns:
        ssim_index : float, mean SSIM
        ssim_map   : 2D array of SSIM values
    """
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions")
    
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)
    
    C1 = (K1*L)**2
    C2 = (K2*L)**2

    gauss = cv.getGaussianKernel(window_size, 1.5)
    window = gauss @ gauss.T

    mu1 = cv.filter2D(img1, -1, window)
    mu2 = cv.filter2D(img2, -1, window)

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv.filter2D(img1**2, -1, window) - mu1_sq
    sigma2_sq = cv.filter2D(img2**2, -1, window) - mu2_sq
    sigma12 = cv.filter2D(img1*img2, -1, window) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    
    ssim_index = np.mean(ssim_map)
    return ssim_index, ssim_map

def compare_boards(img1_file, img2_file, comparison_filename=None):
    """Compare two boards using SSIM.
    The output is an image showing the differences between the two images.
    Parameters:
    - img1_file, the golden board.
    - img2_file, a test board of same board type as the golden board.

    Displays: Image showing regions that differ the most between the two input images.
    Return: Currently none
    """
    img1 = cv.imread(img1_file)
    img2 = cv.imread(img2_file)

    if img1 is None or img2 is None:
        print(f"Image 1 (gold) filepath: {img1_file}")
        print(f"Image 2 (gold) filepath: {img2_file}")
        raise FileNotFoundError("One or both images not found. Make sure 'golden.jpg' and 'test#.jpg' are in boards folder!")

    # --- Resize to same dimensions ---
    h = min(img1.shape[0], img2.shape[0])
    w = min(img1.shape[1], img2.shape[1])
    img1 = cv.resize(img1, (w, h))
    img2 = cv.resize(img2, (w, h))

    # --- Downscale → blur → upscale trick ---
    def smooth_blur(img, scale=0.25, kernel=(15, 15), sigma=00):
        small = cv.resize(img, (0, 0), fx=scale, fy=scale)
        blurred_small = cv.GaussianBlur(small, kernel, sigma)
        return cv.resize(blurred_small, (img.shape[1], img.shape[0]))

    blur1 = smooth_blur(img1)
    blur2 = smooth_blur(img2)

    # --- Convert to grayscale for SSIM ---
    gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    gray_blur1 = cv.cvtColor(blur1, cv.COLOR_BGR2GRAY)
    gray_blur2 = cv.cvtColor(blur2, cv.COLOR_BGR2GRAY)

    # --- Compute SSIM difference maps ---
    score_orig, diff_originals = ssim(gray1, gray2)
    score_blur, diff_blurred = ssim(gray_blur1, gray_blur2)

    # Invert SSIM to show differences
    diff_originals = 1 - diff_originals
    diff_blurred = 1 - diff_blurred

    # Normalize for visualization
    diff_originals = cv.normalize(diff_originals, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
    diff_blurred = cv.normalize(diff_blurred, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)

    print(f"SSIM (Originals): {score_orig:.4f}")
    print(f"SSIM (Blurred):  {score_blur:.4f}")

    inferno = cv.applyColorMap(diff_blurred, cv.COLORMAP_INFERNO)
    # cv.imwrite("./images/board_inferno.jpg", inferno)

    while(True):
        cv.imshow('difference', inferno)
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            for i in range(4):
                cv.waitKey(1)
            break

    '''Save the file'''
    if comparison_filename is not None:
        cv.imwrite(comparison_filename, inferno)

# compare_boards("./images/board_golden.jpg", "./images/board_test.jpg")
