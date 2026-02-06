import cv2

points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        points.append((x,y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"{x},{y}", (x, y), font, 4, (255, 0, 0), 12)
        cv2.imshow('image', img)

    if event == cv2.EVENT_RBUTTONDOWN:
        print(x, y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        b, g, r = img[y, x]
        cv2.putText(img, f"{b},{g},{r}", (x, y), font, 4, (255, 255, 0), 12)
        cv2.imshow('image', img)

def crop_image(image_file):
    x1, y1 = points[0]
    x2, y2 = points[1]
    print(x1, y1)
    print(x2, y2)
    cropped_img = image_file[y1:y2, x1:x2]
    cv2.imshow("cropped", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('cropped.jpg', cropped_img)

if __name__=="__main__":
    img = cv2.imread('../img_compare/test_c/circuit1_c.JPG', 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    crop_image(img)
