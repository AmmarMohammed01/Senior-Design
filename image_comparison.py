# image_comparison.py
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

def compare_boards():
    """Compare two boards"""
    # board1 = cv.imread("Board1.png", cv.IMREAD_GRAYSCALE)
    # board2 = cv.imread("Board2.png", cv.IMREAD_GRAYSCALE)
    # board1 = cv.imread("../learn/opencv/images/board_golden.jpg", cv.IMREAD_GRAYSCALE)
    # board2 = cv.imread("../learn/opencv/images/board_test.jpg", cv.IMREAD_GRAYSCALE)
    board1 = cv.imread("../learn/opencv/images/board_golden.jpg")
    board2 = cv.imread("../learn/opencv/images/board_test.jpg")

    # Apply blur
    board1 = cv.GaussianBlur(board1, (15,15), 0)
    board2 = cv.GaussianBlur(board2, (15,15), 0)

    board1 = cv.cvtColor(board1, cv.COLOR_BGR2GRAY)
    board2 = cv.cvtColor(board2, cv.COLOR_BGR2GRAY)

    score, diff = ssim(board1, board2, full=True)
    print(f"SSIM Score: {score}")
    print(type(diff))
    print(diff.shape)
    print(diff.dtype)

    # Normalize diff image to 0–255 for applyColorMap
    # b/c diff was float64 with each pixel value range [0,1], we need uint8 range [0,255] for each grayscale pixel
    diff = (diff * 255).astype("uint8")
    diff = 1 - diff
    inferno = cv.applyColorMap(diff, cv.COLORMAP_INFERNO)

    cv.imshow('difference', inferno)
    if cv.waitKey(0) == ord('q'):
        cv.destroyAllWindows()

    # cv.imwrite("SSIM_with_blur2_grayAfterBlur_inferno.jpg", inferno)
