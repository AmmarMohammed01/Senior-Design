import cv2 as cv

camera_index = 0

cap = cv.VideoCapture(camera_index)

cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("Cannot open camera")
    return


current_w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
current_h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
print(f"Current Resolution: {int(current_w)}x{int(current_h)}")

image_num = 1
while True:
    filename = str(image_num) + '.jpg'
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame.")
        break

    cv.imshow('Capture', frame)

    key = cv.waitKey(1)

    if key == ord('c'):
        print(f'Image Captured {filename}')
        cv.imwrite(filename, frame)

    if key == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
for i in range(4):
    cv.waitKey(1)
