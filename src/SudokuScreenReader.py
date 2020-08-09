import cv2
import math
import numpy as np
from imutils import contours

import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class SudokuScreenReader:

    def __init__(self):

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

    def take_screenshot(self, x, y, w, h):
        im1 = pyautogui.screenshot(region=(x, y, w, h))
        open_cv_image = np.array(im1)
        self.image = open_cv_image[:, :, ::-1].copy()
        self.get_image_characteristics()

    def get_image_characteristics(self):
        self.image_height, self.image_width, self.image_channels = self.image.shape
        self.cell_size = int(self.image_width / 9) | 1
        self.min_cell_size = int(self.image_width / 20 * self.image_width / 20)
        self.max_cell_size = int(self.image_width / 9 * self.image_width / 9)

    def find_original_contours(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.thresh_invert = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                   int(self.cell_size), 5)
        self.thresh_orig = 255 - self.thresh_invert

        # Find the contours
        orig_contours = cv2.findContours(self.thresh_invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        orig_contours = orig_contours[0] if len(orig_contours) == 2 else orig_contours[1]
        for block in orig_contours:
            area = cv2.contourArea(block)
            if area < self.min_cell_size:
                cv2.drawContours(self.thresh_invert, [block], -1, (0, 0, 0), -1)

    def fix_straight_lines(self):
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        self.thresh_invert = cv2.morphologyEx(self.thresh_invert, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        self.thresh_invert = cv2.morphologyEx(self.thresh_invert, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

    def sort_filtered_contours(self):
        # Sort by top to bottom and each row by left to right
        invert = 255 - self.thresh_invert
        real_contours = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        real_contours = real_contours[0] if len(real_contours) == 2 else real_contours[1]

        for i, c in enumerate(real_contours, 1):
            contour_area = cv2.contourArea(c)
            if self.min_cell_size < contour_area < self.max_cell_size:
                self.good_contours.append(c)
        self.board_dimension = int(math.sqrt(len(self.good_contours)))

        (half_sorted_contours, _) = contours.sort_contours(self.good_contours, method="top-to-bottom")

        row = []
        for i, c in enumerate(half_sorted_contours, 1):
            row.append(c)
            if i % self.board_dimension == 0:
                (full_sorted_contours, _) = contours.sort_contours(row, method="left-to-right")
                self.game_board_contours.append(full_sorted_contours)
                row = []

    def read_board_values(self):
        # Iterate through each box
        for row in self.game_board_contours:
            board_row = []
            for c in row:
                x, y, w, h = cv2.boundingRect(c)
                x_margin = int(w * 0.05)
                y_margin = int(h * 0.05)
                cropped_image = self.thresh_orig[y + y_margin:y + h - 2 * y_margin, x + x_margin:x + w - 2 * x_margin]
                if np.average(cropped_image) > 253:
                    board_row.append(0)
                else:
                    board_row.append(pytesseract.image_to_string(cropped_image, config=self.pytesseract_config))
            self.game_board.append(board_row)

    def convert_to_numbers(self):
        for i, row in enumerate(self.game_board):
            for j, character in enumerate(row):
                if character != 0 and character.isdigit():
                    self.game_board[i][j] = int(character)

    def get_sudoku_board(self, x, y, w, h):
        self.take_screenshot(x, y, w, h)
        self.find_original_contours()
        self.fix_straight_lines()
        self.sort_filtered_contours()
        self.read_board_values()
        self.convert_to_numbers()


if __name__ == "__main__":
    reader = SudokuScreenReader()
    reader.get_sudoku_board(220, 320, 450, 450)

