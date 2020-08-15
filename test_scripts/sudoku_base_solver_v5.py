# Solves via heuristics

import time
import numpy as np
from itertools import combinations


binary_to_real = {
    1: 9,       2: 8,       4: 7,
    8: 6,       16: 5,      32: 4,
    64: 3,      128: 2,     256: 1
}

binary_rep = [0b100000000, 0b010000000, 0b001000000, 0b000100000, 0b000010000, 0b000001000, 0b000000100,
              0b000000010, 0b000000001]


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
        self.candidate_list = np.zeros((self.rows, self.cols), dtype=int)

    def block_top_left(self, x, y):
        top_x = (x // self.block_size) * self.blocks_across
        top_y = (y // self.block_size) * self.blocks_across
        return top_x, top_y

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

                valid_candidates = 0b0
                if self.board[i][j] == 0:
                    for candidate in range(1, 10):
                        valid_candidates = valid_candidates << 1
                        if self.is_valid_board(i, j, candidate):
                            valid_candidates += 0b1

                self.candidate_list[i][j] = valid_candidates

    def insert_value_and_update_candidate_list(self, binary_value, x, y):
        decimal_value = binary_to_real[binary_value]
        self.board[x][y] = decimal_value

        for i, candidates in enumerate(self.candidate_list[x, :]):
            self.candidate_list[x, i] = candidates & (~binary_value & 0b111111111)

        for j, candidates in enumerate(self.candidate_list[:, y]):
            self.candidate_list[j, y] = candidates & (~binary_value & 0b111111111)

        top_x, top_y = self.block_top_left(x, y)
        for i in range(top_x, top_x + 3):
            for j in range(top_y, top_y + 3):
                self.candidate_list[i, j] = self.candidate_list[i][j] & (~binary_value & 0b111111111)

    def solve_naked_singles(self):
        modified_board = False
        for i in range(self.rows):
            for j in range(self.cols):
                if bin(self.candidate_list[i][j]).count("1") == 1:
                    self.insert_value_and_update_candidate_list(self.candidate_list[i][j], i, j)
                    modified_board = True
        return modified_board

    def solve_hidden_sets(self):
        candidate_list_copy = self.candidate_list.copy()
        for i in range(1, 9):
            self.solve_hidden_sets_rows(i)
            self.solve_hidden_sets_cols(i)
            self.solve_hidden_sets_blocks(i)
        return not np.array_equal(candidate_list_copy, self.candidate_list)

    def solve_hidden_sets_rows(self, hidden_rate):
        for i, row in enumerate(self.candidate_list):

            # Make sure that we're not finding combinations of all the remaining empty cells
            non_zeros = np.where(self.board[i, :] == 0)[0]
            if len(non_zeros) <= hidden_rate:
                continue

            values = None
            col_cells = None

            # Go through all combinations of size hidden_rate of nonzero cells
            # Take the union, if the set size after the union is equivalent to the number of cells
            # Then we have found a naked set (which is the conjugate of a hidden set of size 9 - n)
            for comb in list(combinations(non_zeros, hidden_rate)):
                base = 0b000000000
                for col in comb:
                    base = base | self.candidate_list[i][col]
                if bin(base).count("1") == hidden_rate:
                    values = base
                    col_cells = comb
                    print("Found number: " + str(bin(base)) + " in position " + str(i) + ", " + str(comb))
                    break

            if values is not None and col_cells is not None:
                for k in range(9):
                    if k not in col_cells:
                        self.candidate_list[i][k] = self.candidate_list[i][k] & (~values & 0b111111111)
        return

    def solve_hidden_sets_cols(self, hidden_rate):
        for i, col in enumerate(self.candidate_list.transpose()):

            # Make sure that we're not finding combinations of all the remaining empty cells
            non_zeros = np.where(self.board[:, i] == 0)[0]
            if len(non_zeros) <= hidden_rate:
                continue

            values = None
            row_cells = None
            for comb in list(combinations(non_zeros, hidden_rate)):
                base = 0b000000000
                for row in comb:
                    base = base | self.candidate_list[row][i]
                if bin(base).count("1") == hidden_rate:
                    values = base
                    row_cells = comb
                    print("Found number: " + str(bin(base)) + " in position " + str(comb) + ", " + str(i))
                    break

            if values is not None and row_cells is not None:
                for k in range(9):
                    if k not in row_cells:
                        self.candidate_list[k][i] = self.candidate_list[k][i] & (~values & 0b111111111)
        return

    def solve_hidden_sets_blocks(self, hidden_rate):
        for x in range(3):
            for y in range(3):
                block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]
                block_board_list = np.reshape(self.board[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

                # Make sure that we're not finding combinations of all the remaining empty cells
                non_zeros = np.where(block_board_list == 0)[0]
                if len(non_zeros) <= hidden_rate:
                    continue

                values = None
                block_cells = None
                for comb in list(combinations(non_zeros, hidden_rate)):
                    base = 0b000000000
                    for cell in comb:
                        base = base | block_candidate_list[cell]
                    if bin(base).count("1") == hidden_rate:
                        values = base
                        block_cells = comb
                        print("Found number: " + str(bin(base)) + " in position " + str(comb) + " in block " + str(x) + ", " + str(y))
                        break

                if values is not None and block_cells is not None:
                    for k in range(9):
                        if k not in block_cells:
                            block_candidate_list[k] = block_candidate_list[k] & (~values & 0b111111111)
                    self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

    def solve_pointing_sets(self):
        candidate_list_copy = self.candidate_list.copy()
        for x in range(3):
            for y in range(3):
                block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

                for num in binary_rep:
                    block_reps = 0b0
                    for candidate in block_candidate_list:
                        block_reps = block_reps << 1
                        if candidate & num > 0:
                            block_reps = block_reps | 0b1
                    if block_reps == 0b110000000 or block_reps == 0b111000000 or block_reps == 0b011000000 or block_reps == 0b101000000:
                        self.eliminate_pointing_row(x, y, num, 0)
                    elif block_reps == 0b000110000 or block_reps == 0b000111000 or block_reps == 0b000011000 or block_reps == 0b000101000:
                        self.eliminate_pointing_row(x, y, num, 1)
                    elif block_reps == 0b000000110 or block_reps == 0b000000111 or block_reps == 0b000000011 or block_reps == 0b000000101:
                        self.eliminate_pointing_row(x, y, num, 2)
                    elif block_reps == 0b100100000 or block_reps == 0b100100100 or block_reps == 0b000100100 or block_reps == 0b100000100:
                        self.eliminate_pointing_col(x, y, num, 0)
                    elif block_reps == 0b010010000 or block_reps == 0b010010010 or block_reps == 0b000010010 or block_reps == 0b010000010:
                        self.eliminate_pointing_col(x, y, num, 1)
                    elif block_reps == 0b001001000 or block_reps == 0b001001001 or block_reps == 0b000001001 or block_reps == 0b001000001:
                        self.eliminate_pointing_col(x, y, num, 2)
        return not np.array_equal(candidate_list_copy, self.candidate_list)

    def eliminate_pointing_row(self, x, y, candidate, sub_row_num):
        print("Block (" + str(x) + ", " + str(y) + ") sub row " + str(sub_row_num) + " number: " + str(candidate))
        row_num = (x * 3) + sub_row_num
        col_num = [y * 3, y * 3 + 1, y * 3 + 2]
        for j, cell in enumerate(self.candidate_list[row_num, :]):
            if j not in col_num:
                self.candidate_list[row_num, j] = cell & (~candidate & 0b111111111)
        return

    def eliminate_pointing_col(self, x, y, candidate, sub_col_num):
        print("Block (" + str(x) + ", " + str(y) + ") sub col " + str(sub_col_num) + " number: " + str(candidate))
        row_num = [x * 3, x * 3 + 1, x * 3 + 2]
        col_num = (y * 3) + sub_col_num
        for i, cell in enumerate(self.candidate_list[:, col_num]):
            if i not in row_num:
                self.candidate_list[i, col_num] = cell & (~candidate & 0b111111111)
        return

    def solve_box_line_reduction(self):
        candidate_list_copy = self.candidate_list.copy()
        self.solve_box_line_reduction_row()
        self.solve_box_line_reduction_col()
        return not np.array_equal(candidate_list_copy, self.candidate_list)

    def solve_box_line_reduction_row(self):
        for i, row in enumerate(self.candidate_list):
            for num in binary_rep:
                row_reps = 0b0
                for candidate in row:
                    row_reps = row_reps << 1
                    if candidate & num > 0:
                        row_reps = row_reps | 0b1
                if row_reps == 0b110000000 or row_reps == 0b111000000 or row_reps == 0b011000000 or row_reps == 0b101000000:
                    self.eliminate_box_row(i, num, 0)
                elif row_reps == 0b000110000 or row_reps == 0b000111000 or row_reps == 0b000011000 or row_reps == 0b000101000:
                    self.eliminate_box_row(i, num, 1)
                elif row_reps == 0b000000110 or row_reps == 0b000000111 or row_reps == 0b000000011 or row_reps == 0b000000101:
                    self.eliminate_box_row(i, num, 2)
        return

    def eliminate_box_row(self, row_num, candidate, box_y_num):
        sub_row_num = row_num % 3
        avoid_cells = [sub_row_num * 3, sub_row_num * 3 + 1, sub_row_num * 3 + 2]
        x = row_num // 3
        y = box_y_num
        block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

        print("Box-row: Box (" + str(x) + ", " + str(y) + ") sub row " + str(sub_row_num) + " number: " + str(candidate))

        for k, cell in enumerate(block_candidate_list):
            if k not in avoid_cells:
                block_candidate_list[k] = block_candidate_list[k] & (~candidate & 0b111111111)
            self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

    def solve_box_line_reduction_col(self):
        for i, col in enumerate(self.candidate_list.transpose()):
            for num in binary_rep:
                col_reps = 0b0
                for candidate in col:
                    col_reps = col_reps << 1
                    if candidate & num > 0:
                        col_reps = col_reps | 0b1
                if col_reps == 0b110000000 or col_reps == 0b111000000 or col_reps == 0b011000000 or col_reps == 0b101000000:
                    self.eliminate_box_col(i, num, 0)
                elif col_reps == 0b000110000 or col_reps == 0b000111000 or col_reps == 0b000011000 or col_reps == 0b000101000:
                    self.eliminate_box_col(i, num, 1)
                elif col_reps == 0b000000110 or col_reps == 0b000000111 or col_reps == 0b000000011 or col_reps == 0b000000101:
                    self.eliminate_box_col(i, num, 2)
        return

    def eliminate_box_col(self, col_num, candidate, box_x_num):
        sub_col_num = col_num % 3
        avoid_cells = [sub_col_num, sub_col_num + 3, sub_col_num + 6]
        x = box_x_num
        y = col_num // 3
        block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

        print("Box-col: Box (" + str(x) + ", " + str(y) + ") sub col " + str(sub_col_num) + " number: " + str(candidate))

        for k, cell in enumerate(block_candidate_list):
            if k not in avoid_cells:
                block_candidate_list[k] = block_candidate_list[k] & (~candidate & 0b111111111)
            self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

    def solve_x_sword_jelly_row(self):
        for num in binary_rep:

            for i, row in enumerate(self.candidate_list):
                


            for comb in list(combinations(non_zeros, hidden_rate)):
                base = 0b000000000
                for cell in comb:
                    base = base | block_candidate_list[cell]

    def solve_sudoku(self):
        start = time.time()
        self.get_candidate_list()
        while np.count_nonzero(self.board) < 81:
            while self.solve_naked_singles():
                print("o")
            self.solve_hidden_sets()
        print(time.time() - start)
        print(self.board)
        return

