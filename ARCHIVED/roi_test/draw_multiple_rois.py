import cv2

# Load the image
img = cv2.imread("board_golden.jpg")
assert img is not None, "Image file not found"

rois = []

while True:
    # Let user select ROI (drag a box)

    user_choice = input("Want to exit ROI drawing process? Y or N")
    if user_choice == "Y":
        print("escape")
        break

    roi = cv2.selectROI("Select ROI", img, False)

    # Extract cropped region
    # cropped_img = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

    # Save and display cropped image
    # cv2.imwrite("Cropped.png", cropped_img)
    # cv2.imshow("Cropped Image", cropped_img)
    rois.append(roi)

print("here")
cv2.destroyAllWindows()
for i in range(4):
    cv2.waitKey(1)
print("there")

print(rois)
