# Solves via heuristics

import time
import numpy as np


class SudokuRecursiveSolver5:

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
        self.candidate_list = None

    def load_board(self, game_board, block_size=3):
        self.board = np.array(game_board)
        self.solution = self.board.copy()
        self.rows, self.cols = self.board.shape
        self.block_size = block_size
        self.blocks_across = int(self.rows / self.block_size)
        self.candidate_list = np.empty((self.rows, self.cols), dtype=list)

    def has_valid_sudoku_constraints(self, x, y, candidate):

        # Checks that the rows are valid
        if candidate in self.board[x, :]:
            return False

        # Checks that the column are valid
        if candidate in self.board[:, y]:
            return False

        # Checks that the blocks are valid
        row_block = (x // 3) * 3
        col_block = (y // 3) * 3
        if candidate in self.board[row_block:row_block + 3, col_block:col_block + 3]:
            return False

        return True

    def is_valid_board(self, x, y, candidate):

        if candidate == -1:
            return True

        if not self.has_valid_sudoku_constraints(x, y, candidate):
            return False

        return True

    def get_candidate_list(self):
        for i in range(self.rows):
            for j in range(self.cols):
                valid_candidates = []
                if self.board[i][j] == 0:
                    for candidate in range(1, 10):
                        if self.is_valid_board(i, j, candidate):
                            valid_candidates.append(candidate)
                self.candidate_list[i][j] = valid_candidates

    def solve_naked_singles(self):
        modified_board = False
        for i in range(self.rows):
            for j in range(self.cols):
                if len(self.candidate_list[i][j]) == 1:
                    self.board[i][j] = self.candidate_list[i][j][0]
                    modified_board = True
        return modified_board

    def solve_hidden_row_single(self):
        modified_board = False
        for i, row in enumerate(self.candidate_list):
            for candidate in range(1, 10):
                appearance_count = 0
                last_appearance = 0
                if candidate not in self.board[i, :]:
                    for j, cell in enumerate(row):
                        if candidate in cell:
                            appearance_count += 1
                            last_appearance = j
                if appearance_count == 1:
                    self.board[i][last_appearance] = candidate
                    modified_board = True
        return modified_board

    def solve_hidden_col_single(self):
        modified_board = False
        for i, col in enumerate(self.candidate_list.transpose()):
            for candidate in range(1, 10):
                appearance_count = 0
                last_appearance = 0
                if candidate not in self.board[:, i]:
                    for j, cell in enumerate(col):
                        if candidate in cell:
                            appearance_count += 1
                            last_appearance = j
                if appearance_count == 1:
                    self.board[last_appearance][i] = candidate
                    modified_board = True
        return modified_board

    def solve_hidden_block_single(self):
        modified_board = False
        for x in range(3):
            for y in range(3):


    def solve_sudoku(self):
        for i in range(2):
            self.get_candidate_list()
            self.solve_naked_singles()
            self.solve_hidden_row_single()
            self.solve_hidden_col_single()
        print(self.board)
