import cv2
from ultralytics import YOLO


# ── Config ─────────────────────────────────────────────────
MODEL_PATH = 'best.pt'   # path to your downloaded best.pt
CONF       = 0.25        # confidence threshold (lower = more detections)
IOU        = 0.45        # overlap threshold for NMS
IMG_SIZE   = 640
# ───────────────────────────────────────────────────────────

# Colours per class (BGR)
CLASS_COLORS = {
    'misaligned':        (0,   165, 255),   # orange
    'missing_component': (0,   0,   255),   # red
    'solder_bridge':     (0,   255, 255),   # yellow
    'tombstone':         (255, 0,   0  ),   # blue
}
DEFAULT_COLOR = (180, 180, 180)


def draw_detections(frame, results):
    """Draw bounding boxes and labels on frame."""
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf  = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = result.names[cls_id]
            color = CLASS_COLORS.get(cls_name, DEFAULT_COLOR)

            # Box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Label background
            label = f"{cls_name}  {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)

            # Label text
            cv2.putText(frame, label, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)

    return frame


def draw_summary(frame, results):
    """Draw a summary box in the top-left corner."""
    counts = {}
    for result in results:
        for box in result.boxes:
            name = result.names[int(box.cls[0])]
            counts[name] = counts.get(name, 0) + 1

    if not counts:
        status = "PASS"
        status_color = (0, 200, 0)
    else:
        status = "FAIL"
        status_color = (0, 0, 220)

    # Background panel
    lines = [f"Status: {status}"] + [f"  {k}: {v}" for k, v in counts.items()]
    panel_h = len(lines) * 22 + 12
    cv2.rectangle(frame, (8, 8), (220, 8 + panel_h), (20, 20, 20), -1)
    cv2.rectangle(frame, (8, 8), (220, 8 + panel_h), status_color, 2)

    for i, line in enumerate(lines):
        color = status_color if i == 0 else (220, 220, 220)
        cv2.putText(frame, line, (14, 28 + i * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)
    return frame


'''
model = YOLO(model_path)
'''
def run_camera(model_path, roi, camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # ── One-time ROI selection ──────────────────────────────
    # print("Draw a rectangle around the board, then press ENTER or SPACE")
    # ret, first_frame = cap.read()
    # roi = cv2.selectROI("Select board area — press ENTER when done",
                         # first_frame, fromCenter=False, showCrosshair=True)
    # cv2.destroyAllWindows()
    x, y, w, h = roi
    # ────────────────────────────────────────────────────────

    print("Live camera running — press Q to quit, S to save")

    model = YOLO(model_path)

    BORDER_THICKNESS = 1 # used to be 5

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop to board only — matching your training images
        cv2.rectangle(frame, (x-BORDER_THICKNESS, y-BORDER_THICKNESS), (x+w+BORDER_THICKNESS, y+h+BORDER_THICKNESS), (0, 255, 0), BORDER_THICKNESS)

        board = frame[y:y+h, x:x+w]

        # Run inference on the cropped board, https://docs.ultralytics.com/modes/predict#inference-arguments
        results = model.predict(board, conf=CONF, iou=IOU, imgsz=IMG_SIZE, verbose=False)
        board = draw_detections(board, results)
        board = draw_summary(board, results)

        # Put the annotated board back into the full frame
        frame[y:y+h, x:x+w] = board

        cv2.imshow('PCB Defect Detection - Live', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite('capture.jpg', board)  # saves just the board crop
            print("Saved capture.jpg")

    cap.release()
    cv2.destroyAllWindows()
    for i in range(4):
        cv2.waitKey(1)
