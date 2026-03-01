"""
FILE: map_errors.py
Contains:
- class YOLOLabel
- def map_errors(heatmap_img_file, golden_board_components_file, golden_board_classes_file)
- def get_YOLO_label(golden_board_components_file)
- def get_YOLO_classes(golden_board_classes_file)
"""

'''NEED:
- Check if YOLO Label file exists before mapping the labels
- Detect labeled regions with the most differences (the most orange)
'''

import cv2 as cv

class YOLOLabel:
    """YOLOLabel stores labels from the YOLO format
    A YOLO label looks like this:
    0 0.418945 0.359375 0.055339 0.088349

    1ST number: class or name of label
    2ND number: x coordinate for the center of the label, shown as percentage of the image width
    3RD number: y coordinate for the center of the label, shown as percentage of the image width
    4TH number: width of the label, shown as percentage of the image width
    5TH number: height of the label, shown as percentage of the image height
    """
    def __init__(self, label_name="", label_x=0.0, label_y=0.0, label_width=0.0, label_height=0.0):
        """YOLOLabel constructor"""
        self.label_name = label_name
        self.label_x = label_x
        self.label_y = label_y
        self.label_width = label_width
        self.label_height = label_height

    def convert_to_label(self, label_coordinates, label_classes):
        """Given a line from the YOLO coordinates YOLO classes files, convert to label object"""
        label_contents = label_coordinates.split()
        self.label_name = label_classes[ int(label_contents[0]) ]
        self.label_x = float(label_contents[1])
        self.label_y = float(label_contents[2])
        self.label_width = float(label_contents[3])
        self.label_height = float(label_contents[4])

    def print_label(self):
        print(f"YOLOLabel contents: {self.label_name}, {self.label_x}, {self.label_y}, {self.label_width}, {self.label_height}")

def map_errors(heatmap_img_file, golden_board_components_file, golden_board_classes_file):
    """Given:
    1. the heatmap of differences between golden and test boards,
    2. the labeled components of the golden board.

    Draw the labels on the heatmap image"""

    heatmap_img = cv.imread(heatmap_img_file) #numpy.ndarray
    height = 0
    width = 0

    if heatmap_img is not None:
        height, width = heatmap_img.shape[:2]
        print(f"height: {height}, width: {width}")
    else:
        print("Heatmap Image not found")
        exit()

    golden_board_component_points = get_YOLO_label(golden_board_components_file)
    golden_board_componennt_names = get_YOLO_classes(golden_board_classes_file)

    # Plot labels onto board heatmap
    if golden_board_component_points and golden_board_componennt_names:
        # print(golden_board_component_points)

        for label_info in golden_board_component_points:
            current_label = YOLOLabel()
            current_label.convert_to_label(label_info, golden_board_componennt_names)

            center_x = current_label.label_x * width
            center_y = current_label.label_y * height
            y1, y2 = center_y - (height * current_label.label_height) / 2, center_y + (height * current_label.label_height) / 2
            x1, x2 = center_x - (width * current_label.label_width) / 2, center_x + (width * current_label.label_width) / 2
            x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
            # print(f"(x1, y1): ({x1}, {y1})   (x2, y2): ({x2}, {y2})")

            cv.rectangle(heatmap_img, (x1, y1), (x2, y2), (0,255,0), 5)

        cv.imshow('heatmap', heatmap_img)
        if cv.waitKey(0) == ord('q'):
            cv.destroyAllWindows()

def get_YOLO_label(golden_board_components_file):
    """Get the YOLO label coordinates"""
    try:
        golden_board_component_points = []
        with open(golden_board_components_file) as f:
            for line in f:
                golden_board_component_points.append(line.strip())
        return golden_board_component_points

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_components_file}' was not found")

def get_YOLO_classes(golden_board_classes_file):
    """Get the YOLO label class names"""
    try:
        golden_board_componennt_names = []
        with open(golden_board_classes_file) as f:
            for line in f:
                golden_board_componennt_names.append(line.strip())
        return golden_board_componennt_names

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_classes_file}' was not found")

# map_errors('./images/board_inferno.jpg', './images/board_golden.txt', './images/classes.txt')

