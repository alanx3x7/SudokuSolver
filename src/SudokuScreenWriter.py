# Necessary imports
import cv2
import math
import numpy as np

# PyAutoGUI imports
import pyautogui


class SudokuScreenWriter:
    """ Class to automatically write in the solution of the sudoku solver to the sudoku puzzle on screen
    """

    def __init__(self):
        """ Constructor """

        # Game image characteristics
        self.image_start_x = None
        self.image_start_y = None
        self.solution_board = None
        self.game_board_contours = None
        self.game_board_centers = None

    def load_solution_board(self, x, y, solution, positions):
        """ Load the solution of the sudoku
            :param x: The x coordinate of the top left of the screenshot location for the sudoku puzzle [int]
            :param y: The y coordinate of the top left of the screenshot location for the sudoku puzzle [int]
            :param solution: The solution to the sudoku puzzle [2D numpy array of int]
            :param positions: The list of contours for each cell in the sudoku puzzle [list of contours]
            :return: None
        """
        self.image_start_x = x
        self.image_start_y = y
        self.solution_board = solution.copy()
        self.game_board_contours = positions

    def find_game_board_centers(self):
        """ Computes the centers of each cell in the sudoku puzzle on the screen via the contours
            :return: None
        """
        self.game_board_centers = []

        # Goes through every contour as each contour corresponds to a cell in the sudoku puzzle
        for i, row in enumerate(self.game_board_contours):
            game_board_center_row = []
            for j, cell in enumerate(row):

                # Compute the center of the cell as the average of all points on the contour
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
        """ Writes the sudoku solution into the on-screen sudoku puzzle
            :return: None
        """

        # Goes through all cells
        for i, row in enumerate(self.game_board_centers):
            for j, cell in enumerate(row):

                # Moves the mouse to the center of that cell, click, and press the number corresponding to the solution
                pyautogui.moveTo(cell[0], cell[1])
                pyautogui.click()
                value = self.solution_board[i][j]
                pyautogui.press(str(value))
