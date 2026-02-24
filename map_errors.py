import cv2 as cv

class MyLabel:
    def __init__(self, label_name="", label_x=0.0, label_y=0.0):
        '''MyLabel constructor'''
        self.label_name = label_name
        self.label_x = label_x
        self.label_y = label_y

    def convert_to_label(self, label_coordinates, label_classes):
        '''Given a line from the YOLO coordinates YOLO classes files, convert to label object'''
        label_contents = label_coordinates.split()
        self.label_name = label_classes[ int(label_contents[0]) ]
        self.label_x = float(label_contents[1])
        self.label_y = float(label_contents[2])

    def print_label(self):
        print(f"MyLabel contents: {self.label_name}, {self.label_x}, {self.label_y}")
        print(type(self.label_name))
        print(type(self.label_x))
        print(type(self.label_y))

def map_errors(heatmap_img_file, golden_board_components_file, golden_board_classes_file):
    '''Given the heatmap of differences between golden and test boards,
    and the labeled components of the golden board,
    draw the labels on the heatmap image'''

    heatmap_img = cv.imread(heatmap_img_file)
    # height, width, channels = heatmap_img.shape
    if heatmap_img is not None:
        height, width = heatmap_img.shape[:2]
        print(f"height: {height}, width: {width}")

    golden_board_component_points = []
    golden_board_componennt_names = []

    try:
        with open(golden_board_components_file) as f:
            # content = f.read()
            # print(content)
            for line in f:
                golden_board_component_points.append(line.strip())

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_components_file}' was not found")

    try:
        with open(golden_board_classes_file) as f:
            for line in f:
                golden_board_componennt_names.append(line.strip())

    except FileNotFoundError:
        print(f"Error: The file '{golden_board_components_file}' was not found")


    if golden_board_component_points and golden_board_componennt_names:
        print(golden_board_component_points)
        label1 = MyLabel()
        label1.convert_to_label(golden_board_component_points[0], golden_board_componennt_names)
        label1.print_label()

        center_x = int(label1.label_x * width)
        center_y = int(label1.label_y * height)

        cv.circle(heatmap_img, (center_x, center_y), 100, (0, 255, 0), 20)

        cv.imshow('heatmap', heatmap_img)
        if cv.waitKey(0) == ord('q'):
            cv.destroyAllWindows()

map_errors('./images/SSIM_with_blur2_grayAfterBlur_inferno.jpg', './images/board_golden.txt', './images/classes.txt')

