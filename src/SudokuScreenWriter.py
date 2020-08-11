import cv2
import math
import numpy as np

import pyautogui


class SudokuScreenWriter:

    def __init__(self):

        # Game image characteristics
        self.image_start_x = None
        self.image_start_y = None
        self.solution_board = None
        self.game_board_contours = None
        self.game_board_centers = None

    def load_solution_board(self, x, y, solution, positions):
        self.image_start_x = x
        self.image_start_y = y
        self.solution_board = solution.copy()
        self.game_board_contours = positions

    def find_game_board_centers(self):
        self.game_board_centers = []
        for i, row in enumerate(self.game_board_contours):
            game_board_center_row = []
            for j, cell in enumerate(row):
                center_x = 0
                center_y = 0
                num_corners = 0
                for k in cell:
                    center_x += k[0][0]
                    center_y += k[0][1]
                    num_corners += 1
                center_x = int(center_x / num_corners)
                center_y = int(center_y / num_corners)
                game_board_center_row.append([int(center_x + self.image_start_x), int(center_y + self.image_start_y)])
            self.game_board_centers.append(game_board_center_row)

    def write_in_sudoku(self):

        for i, row in enumerate(self.game_board_centers):
            for j, cell in enumerate(row):
                pyautogui.moveTo(cell[0], cell[1])
                pyautogui.click()
                value = self.solution_board[i][j]
                pyautogui.press(str(value))
