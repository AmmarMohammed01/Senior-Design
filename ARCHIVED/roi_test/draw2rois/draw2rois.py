import cv2
 
# Load the image
img = cv2.imread("board_golden.jpg")
assert img is not None, "Image file not found"

# Let user select ROI (drag a box)
roi = cv2.selectROI("Select ROI", img, False)

# Extract cropped region
cropped_img = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

roi = cv2.selectROI("Select ROI", img, False)
cropped_img1 = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

# Save and display cropped image
cv2.imwrite("Cropped.png", cropped_img)
cv2.imshow("Cropped Image", cropped_img)

cv2.imwrite("Cropped1.png", cropped_img1)
cv2.imshow("Cropped Image 1", cropped_img1)

cv2.waitKey(0)
cv2.destroyAllWindows()
