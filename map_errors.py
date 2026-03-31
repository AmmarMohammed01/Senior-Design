"""
FILE: map_errors.py
Contains:
- class YOLOLabel
    - def convert_to_label(self, label_coordinates, label_classes)
    - def print_label(self)
- def map_errors(heatmap_img_file, golden_board_components_file, golden_board_classes_file, golden_board_img_file)
- def get_YOLO_label(golden_board_components_file)
- def get_YOLO_classes(golden_board_classes_file)
- def detect_possible_defect(img, x1, y1, x2, y2) 
- def suggest_defect_type()
"""

'''NEED:
- Check if YOLO Label file exists before mapping the labels
- Detect labeled regions with the most differences (the most orange)
'''

import cv2 as cv
import numpy as np

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
        """Given a line each from the YOLO coordinates & the YOLO classes files, convert to label object"""
        label_contents = label_coordinates.split()
        self.label_name = label_classes[ int(label_contents[0]) ]
        self.label_x = float(label_contents[1])
        self.label_y = float(label_contents[2])
        self.label_width = float(label_contents[3])
        self.label_height = float(label_contents[4])

    def print_label(self):
        print(f"YOLOLabel contents: {self.label_name}, {self.label_x}, {self.label_y}, {self.label_width}, {self.label_height}")

def map_errors(heatmap_img_file, golden_board_components_file, golden_board_classes_file, golden_board_img_file):
    """Given:
    1. the heatmap of differences between golden and test boards,
    2. the YOLO labels of the golden board's components,
    3. the YOLO class names of the labels of the components,
    4. the original golden board image

    Draw the rectangle region labels on the heatmap image, representing the components.
    See what rectangle regions have the highest differences detected
    (meaning which regions have the highest orange color within a threshold)
    and mark those regions as possibly defective.
    Finally overlay the possibly defective regions over the original golden board image.
    """

    golden_board_img = cv.imread(golden_board_img_file)
    assert golden_board_img is not None, "Error: Golden board image not found."
    overlay = golden_board_img.copy()

    '''Import heatmap image and get dimensions'''
    heatmap_img = cv.imread(heatmap_img_file) #numpy.ndarray
    height = 0
    width = 0

    if heatmap_img is not None:
        height, width = heatmap_img.shape[:2]
        print(f"height: {height}, width: {width}")
    else:
        print("Heatmap Image not found")
        exit()

    '''Get the labels coordinates and names from text files and store as list'''
    golden_board_component_points = get_YOLO_label(golden_board_components_file)
    golden_board_componennt_names = get_YOLO_classes(golden_board_classes_file)

    '''Plot labels onto board heatmap'''
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
            has_possible_defect = detect_possible_defect(heatmap_img, x1, y1, x2, y2)
            has_possible_defect_str = "potential defect" if has_possible_defect == True else "good"
            print(f"{current_label.label_name}: {has_possible_defect_str}")

            '''Overlay the possibly defective regions onto the golden board image'''
            if has_possible_defect:
                cv.rectangle(overlay, (x1, y1), (x2, y2), (0,0,255), -1)
                overlay = cv.addWeighted(overlay, 0.8, golden_board_img, 1 - 0.8, 0)


        cv.imshow('heatmap', heatmap_img)
        cv.imshow('golden_board', overlay)

        while True:
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                for i in range(4):
                    cv.waitKey(1)
                break

def get_YOLO_label(golden_board_components_file):
    """Get the YOLO label coordinates
    Given .txt file
    Returns a list"""
    try:
        golden_board_component_points = []
        with open(golden_board_components_file) as f:
            for line in f:
                golden_board_component_points.append(line.strip())
        return golden_board_component_points

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_components_file}' was not found")

def get_YOLO_classes(golden_board_classes_file):
    """Get the YOLO label class names
    Given .txt file
    Returns a list"""
    try:
        golden_board_componennt_names = []
        with open(golden_board_classes_file) as f:
            for line in f:
                golden_board_componennt_names.append(line.strip())
        return golden_board_componennt_names

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_classes_file}' was not found")

def detect_possible_defect(img, x1, y1, x2, y2):
    """
    Look at the ROI for a given component/label, see if orange color above certain threshold is detected, mark region as defect/good.
    Given ROI (Region of Image)
        - x1: top left x
        - y1: top left y
        - x2: bottom right x
        - y2: bottom right y
    Return Possible Defect Exists  = True or False

    SUMMARY:
    In other words, it takes the heat-map comparison image.
    It looks at only one component (one labeled rectangle region).
    It sees if it has a high intensity orange color. If true, then mark potentially defective.
    """

    '''Read Image & Get ROI'''
    # img = cv.imread('image.jpg')
    assert img is not None, "Error: Image not found or could not be read"
    roi = img[y1:y2, x1:x2]

    '''Find orange value in ROI'''
    lower_orange = np.array([0, 100, 100])
    upper_orange = np.array([20, 255, 255])

    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_roi, lower_orange, upper_orange)

    result = cv.bitwise_and(hsv_roi, hsv_roi, mask=mask)
    # cv.imshow('roi', roi)
    # cv.imshow('orange in roi', result)

    result = cv.cvtColor(result, cv.COLOR_HSV2BGR) # without this, display is yellow, doesn't affect mask summation just imshow
    combined_image = cv.hconcat([roi, result])
    cv.imshow('comparison', combined_image)

    if cv.waitKey(0) == ord('q'):
        cv.destroyAllWindows()

    '''If found return defect, else return good'''
    if np.sum(mask) > 0:
        return True # defect
    else:
        return False # good

def suggest_defect_type(region_name):
    """Given a labeled region's/component's name
    Return potential defects associated with component"""

    '''
    Defects discussed 10/21/2025

    What we're looking to detect in the PCB:
    Misalignment - Wrong Installation
    Missing Component
    Wrong Component
    Solder Bridge
    Missing Solder
    Bad Solder Joint
    Broken Trace
    '''

    defect_types = {
        "resistor": ['misalligned', 'missing'],
        "diode": ['misalligned', 'missing', 'part orientation'],
        "capacitor": ['misalligned', 'missing', 'part orientation'],
        "inductor": ['misalligned', 'missing'],
        "smd": ['misalligned', 'missing', 'part orientation', 'solder bridge'],
        "trace": ['broken', 'solder bridge']
    }

    return defect_types[region_name]

def generate_defect_frequency_map(yolo_coordinates_filepath, selected_board_dir, golden_board_filepath, yolo_classes_filepath):
    """Generate defect frequency map"""

    '''Get number of components labeled
    - count number of lines in text file'''
    with open(yolo_coordinates_filepath, 'r') as f:
        num_of_components = sum(1 for line in f)
    print(f"Total number of components: {num_of_components}") # found out Python doesn't have block scope for variables (if/for/while/with), LEGB scope in Python, it does have enclosed/function scope

    '''Create dictionary: key for each component, each value is a defect counter'''
    component_keys = list(range(num_of_components))
    component_defect_frequency = {component: 0 for component in component_keys}
    print(component_defect_frequency)

    comparison_img_files = list(selected_board_dir.glob("compare*.jpg"))

    golden_board_component_points = get_YOLO_label(yolo_coordinates_filepath)
    golden_board_componennt_names = get_YOLO_classes(yolo_classes_filepath)

    '''Open a comparison file, increment counter for each component'''
    for comparison_image_file in comparison_img_files:
        print(comparison_image_file)

        comparison_img = cv.imread(comparison_image_file)
        assert comparison_img is not None, "Error: Golden Board Image Not Found"
        height = 0
        width = 0

        if comparison_img is not None:
            height, width = comparison_img.shape[:2]
            print(f"height: {height}, width: {width}")
        else:
            print("Heatmap Image not found")
            exit()

        if golden_board_component_points and golden_board_componennt_names:
            # print(golden_board_component_points)

            for index, label_info in enumerate(golden_board_component_points):
                current_label = YOLOLabel()
                current_label.convert_to_label(label_info, golden_board_componennt_names)

                center_x = current_label.label_x * width
                center_y = current_label.label_y * height
                y1, y2 = center_y - (height * current_label.label_height) / 2, center_y + (height * current_label.label_height) / 2
                x1, x2 = center_x - (width * current_label.label_width) / 2, center_x + (width * current_label.label_width) / 2
                x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
                # print(f"(x1, y1): ({x1}, {y1})   (x2, y2): ({x2}, {y2})")

                # cv.rectangle(heatmap_img, (x1, y1), (x2, y2), (0,255,0), 5)
                has_possible_defect = detect_possible_defect(comparison_img, x1, y1, x2, y2)
                if has_possible_defect:
                    component_defect_frequency[index] += 1
                # has_possible_defect_str = "potential defect" if has_possible_defect == True else "good"
                # print(f"{current_label.label_name}: {has_possible_defect_str}")


    '''Display counter on center of each component overlayed on golden board image'''
    golden_board_img = cv.imread(golden_board_filepath)
    assert golden_board_img is not None, "Error: Golden Board Image Not Found"
    height = 0
    width = 0

    if golden_board_img is not None:
        height, width = golden_board_img.shape[:2]
        print(f"height: {height}, width: {width}")
    else:
        print("Heatmap Image not found")
        exit()

    # golden_board_component_points = get_YOLO_label(yolo_coordinates_filepath)
    # golden_board_componennt_names = get_YOLO_classes(yolo_classes_filepath)

    if golden_board_component_points and golden_board_componennt_names:
        for index, label_info in enumerate(golden_board_component_points):
            current_label = YOLOLabel()
            current_label.convert_to_label(label_info, golden_board_componennt_names)

            center_x = current_label.label_x * width
            center_y = current_label.label_y * height

            cv.putText(golden_board_img, str(component_defect_frequency[index]), (int(center_x), int(center_y)), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA) 

    cv.imshow('Frequency Map', golden_board_img)
    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            for i in range(4):
                cv.waitKey(1)
            break

# map_errors('./images/board_inferno.jpg', './images/board_golden.txt', './images/classes.txt')
# map_errors('./images/board_inferno.jpg', './images/board_golden.txt', './images/classes.txt', './images/board_golden.jpg')
