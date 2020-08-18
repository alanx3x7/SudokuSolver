# Necessary imports
import cv2
import math
import numpy as np
from imutils import contours

# PyAutoGUI and PyTesseract imports
import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class SudokuScreenReader:
    """ Class to get a screenshot of the sudoku puzzle on screen and read the digits within the grid
    """

    def __init__(self):
        """ Constructor
        """

        # Game image characteristics
        self.image_height = 0
        self.image_width = 0
        self.image_channels = 0
        self.good_contours = []
        self.game_board_contours = []

        # Game board characteristics
        self.game_board = []
        self.board_dimension = 0
        self.cell_size = 0
        self.min_cell_size = 0
        self.max_cell_size = 0

        # Game images
        self.image = None
        self.thresh_invert = None
        self.thresh_orig = None

        # Pytesseract settings
        self.pytesseract_config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 10'

        # Common mis-recognitions for pytesseract
        self.replacements = {'be': '5', 'Cc': 'C', 'Rg': '8', 'i': '1', '':'9'}

    def take_screenshot(self, x, y, w, h, open_cv_image=None):
        """ Takes a screenshot of the screen with coordinates (x, y) and width and height (w, h)
            If an OpenCV image is passed as an argument, that is taken as the screenshot instead
            :param x: The x coordinate of the top left corner of the screenshot location [int]
            :param y: The y coordinate of the top left corner of the screenshot location [int]
            :param w: The width of the area to be taken a screenshot of [int]
            :param h: The height of the area to be taken a screenshot of [int]
            :param open_cv_image: A OpenCV Mat of the screenshot [CV::Mat or 3-channel 2D numpy array of int]
            :return: None
        """

        # If no screenshot image is passed in, take a screenshot at the specified location
        if open_cv_image is None:
            im1 = pyautogui.screenshot(region=(x, y, w, h))
            open_cv_image = np.array(im1)

        # Convert the image from RGB to BGR (OpenCV) format
        self.image = open_cv_image[:, :, ::-1].copy()
        self.get_image_characteristics()

    def get_image_characteristics(self):
        """ Gets the characteristics of the screenshot image taken
            :return: None
        """
        self.image_height, self.image_width, self.image_channels = self.image.shape

        # Estimate the cell size to be around a ninth of the width of the screenshot area
        self.cell_size = int(self.image_width / 9) | 1

        # Cell size should be at most a ninth of the width and at least a twentieth of the width of the screenshot
        # Since a typical grid is 9x9, so it should be at most a ninth of the image width, and it shouldn't be too small
        self.min_cell_size = int(self.image_width / 20 * self.image_width / 20)
        self.max_cell_size = int(self.image_width / 9 * self.image_width / 9)

    def find_original_contours(self):
        """ Gets the contours of the image to find the location of the lines
            :return: None
        """

        # Convert to gray, threshold and invert the image. Also save a thresholded but non-inverted image copy
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.thresh_invert = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                   int(self.cell_size), 5)
        self.thresh_orig = 255 - self.thresh_invert

        # Find the contours of the image. Each contour should correspond to a cell
        orig_contours = cv2.findContours(self.thresh_invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        orig_contours = orig_contours[0] if len(orig_contours) == 2 else orig_contours[1]
        for block in orig_contours:
            area = cv2.contourArea(block)

            # If the contours are not too large, we draw them over the image to remove the digits in the grid
            if area < self.min_cell_size:
                cv2.drawContours(self.thresh_invert, [block], -1, (0, 0, 0), -1)

    def fix_straight_lines(self):
        """ Apply binary closing to straighten out grid lines within the image
            We can do this because we know that the lines of the grid should be straight
            :return: None
        """

        # Creates a vertical 1x5 kernel and applies binary closing based on that kernel
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        self.thresh_invert = cv2.morphologyEx(self.thresh_invert, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)

        # Creates a horizontal 5x1 kernel and applies binary closing based on that kernel
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        self.thresh_invert = cv2.morphologyEx(self.thresh_invert, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

    def sort_filtered_contours(self):
        """ Re-finds the contours in the corrected image and sorts them top-down, left-right
            Each contour should correspond to a cell in the sudoku puzzle
            :return: None
        """

        # Get the contours again
        invert = 255 - self.thresh_invert
        real_contours = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        real_contours = real_contours[0] if len(real_contours) == 2 else real_contours[1]

        # Make sure that they're within the correct range for size
        # If too small, it is probably noise; if too large, then should be things around the grid
        for i, c in enumerate(real_contours, 1):
            contour_area = cv2.contourArea(c)
            if self.min_cell_size < contour_area < self.max_cell_size:
                self.good_contours.append(c)

        # We assume a square board, so the number of rows/cols should be the square root of total contours/cells
        self.board_dimension = int(math.sqrt(len(self.good_contours)))

        # Sort the contours from top to bottom
        (half_sorted_contours, _) = contours.sort_contours(self.good_contours, method="top-to-bottom")

        # We then sort each row from left to right
        row = []
        for i, c in enumerate(half_sorted_contours, 1):
            row.append(c)
            if i % self.board_dimension == 0:
                (full_sorted_contours, _) = contours.sort_contours(row, method="left-to-right")
                self.game_board_contours.append(full_sorted_contours)
                row = []

    def read_board_values(self):
        """ Use the OCR to read each digit from the sudoku board
            :return: None
        """

        # Iterate through each contour/cell
        for row in self.game_board_contours:
            board_row = []

            # For each cell, we get its location and crop the original thresholded image to that location
            for c in row:
                x, y, w, h = cv2.boundingRect(c)
                x_margin = int(w * 0.05)
                y_margin = int(h * 0.05)
                cropped_image = self.thresh_orig[y + y_margin:y + h - 2 * y_margin, x + x_margin:x + w - 2 * x_margin]

                # If it's mostly white, we don't need to waste time with OCR and we know it is blank
                if np.average(cropped_image) > 253:
                    board_row.append(0)

                # Otherwise we pass it to the OCR to see which character is present within that cell
                else:
                    character = pytesseract.image_to_string(cropped_image, config=self.pytesseract_config)
                    # If the character is a commonly mis-read one, use dictionary to find the real character
                    if character in self.replacements:
                        character = self.replacements[character]
                    board_row.append(character)
            self.game_board.append(board_row)

    def convert_to_numbers(self):
        """ Converts OCR string output into int representation
            :return: None
        """
        for i, row in enumerate(self.game_board):
            for j, character in enumerate(row):
                if character != 0 and character.isdigit():
                    self.game_board[i][j] = int(character)

    def clear_for_new_board(self):
        """ Clears member variables to process the next image
            :return: None
        """
        self.game_board = []
        self.good_contours = []
        self.game_board_contours = []

    def get_sudoku_board(self, x, y, w, h, open_cv_image=None):
        """ Main function to help with functionality and usage of the class object. Clears old data, takes the
            screenshot, and processes the image with OCR to find and convert the digits in the sudoku board into
            integers and saves those into the game_board member variable
            :param x: x coordinate of the capture widget/location of screenshot [int]
            :param y: y coordinate of the capture widget/location of screenshot [int]
            :param w: width of the capture widget/screenshot [int]
            :param h: height of the capture widget/screenshot [int]
            :param open_cv_image: A screenshot of the board [CV::Mat object or 3-channel 2D numpy array of int]
            :return: None
        """
        self.clear_for_new_board()
        self.take_screenshot(x, y, w, h, open_cv_image)
        self.find_original_contours()
        self.fix_straight_lines()
        self.sort_filtered_contours()
        self.read_board_values()
        self.convert_to_numbers()
