# Tries to optimize guessing by sorting cells by most seen in row, col, and block
# Much slower than version 3 unfortunately

import time
import numpy as np


class SudokuRecursiveSolver4:

    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.block_size = 0
        self.blocks_across = 0

        self.board = None
        self.solution = None
        self.row_list = None
        self.col_list = None
        self.block_list = None
        self.priority_grid = None
        self.priority_list = []

    def load_board(self, game_board, block_size=3):
        self.board = np.array(game_board)
        self.solution = self.board.copy()
        self.rows, self.cols = self.board.shape
        self.block_size = block_size
        self.blocks_across = int(self.rows / self.block_size)
        self.convert_board_to_string_list()
        self.get_priority_list()

    def get_priority_list(self):
        self.priority_grid = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    row_count = np.count_nonzero(self.board[i, :])
                    col_count = np.count_nonzero(self.board[:, j])
                    row_block = (i // 3) * 3
                    col_block = (j // 3) * 3
                    block_count = np.count_nonzero(self.board[row_block:row_block + 3, col_block:col_block + 3])
                    self.priority_grid[i][j] = row_count + col_count + block_count

        # print(self.priority_grid)
        max_to_min = np.argsort(self.priority_grid, axis=None)#[::-1]
        for i in range(len(max_to_min)):
            x = max_to_min[i] // self.rows
            y = max_to_min[i] % self.cols
            self.priority_list.append([x, y])

    def convert_board_to_string_list(self):

        self.row_list = []
        self.col_list = []
        self.block_list = ["", "", "", "", "", "", "", "", ""]

        for i in range(9):
            row = ""
            col = ""
            for j in range(9):
                row += str(int(self.board[i][j]))
                col += str(int(self.board[j][i]))
            self.row_list.append(row)
            self.col_list.append(col)

        for i in range(9):
            for j in range(9):
                block = 3 * (i // 3) + (j // 3)
                self.block_list[block] += str(int(self.board[i][j]))

    def insert_candidate_into_lists(self, x, y, candidate):
        b = 3 * (x // 3) + (y // 3)
        p = (x % 3) * 3 + (y % 3)
        self.row_list[x] = self.row_list[x][:y] + candidate + self.row_list[x][y + 1:]
        self.col_list[y] = self.col_list[y][:x] + candidate + self.col_list[y][x + 1:]
        self.block_list[b] = self.block_list[b][:p] + candidate + self.block_list[b][p + 1:]

    def has_valid_sudoku_constraints(self, x, y, candidate):

        # Checks that the rows are valid
        if candidate in self.row_list[x]:
            return False

        # Checks that the column are valid
        if candidate in self.col_list[y]:
            return False

        # Checks that the blocks are valid
        block_num = 3 * (x // 3) + (y // 3)
        if candidate in self.block_list[block_num]:
            return False

        return True

    def is_valid_board(self, x, y, candidate):

        if candidate == -1:
            return True

        if not self.has_valid_sudoku_constraints(x, y, candidate):
            return False

        self.insert_candidate_into_lists(x, y, candidate)

        return True

    def recursive_solve(self, x, y, candidate):

        if not self.is_valid_board(x, y, candidate):
            return None

        for i, j in self.priority_list:

            if self.row_list[i][j] != '0':
                continue

            for candidate in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if self.recursive_solve(i, j, candidate) is not None:
                    return True
            self.insert_candidate_into_lists(i, j, '0')
            return None

        return True

    def solve_sudoku(self):
        if self.recursive_solve(0, 0, -1):
            for i, row in enumerate(self.row_list):
                for j, value in enumerate(row):
                    self.solution[i][j] = int(value)
        else:
            print("Failed to solve the sudoku!")
