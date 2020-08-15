# Introduces heuristic approaches to decrease the number of paths for recursive solving

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


def binary_string_to_candidates(binary):
    candidates = ""
    for i, rep in enumerate(binary_rep):
        if binary & rep > 0:
            candidates += str(i + 1)
    return candidates


class SudokuRecursiveSolver:

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
        self.candidate_string_list = None

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

###################################################################################################
###################################################################################################
###################################################################################################

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

###################################################################################################
###################################################################################################
###################################################################################################

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
                        print("Found number: " + str(bin(base)) + " in position " + str(comb) + " in block " +
                              str(x) + ", " + str(y))
                        break

                if values is not None and block_cells is not None:
                    for k in range(9):
                        if k not in block_cells:
                            block_candidate_list[k] = block_candidate_list[k] & (~values & 0b111111111)
                    self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

###################################################################################################
###################################################################################################
###################################################################################################

    def solve_pointing_sets(self):
        candidate_list_copy = self.candidate_list.copy()
        for x in range(3):
            for y in range(3):
                block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

                for num in binary_rep:
                    b_rep = 0b0
                    for candidate in block_candidate_list:
                        b_rep = b_rep << 1
                        if candidate & num > 0:
                            b_rep = b_rep | 0b1
                    if b_rep == 0b110000000 or b_rep == 0b111000000 or b_rep == 0b011000000 or b_rep == 0b101000000:
                        self.eliminate_pointing_row(x, y, num, 0)
                    elif b_rep == 0b000110000 or b_rep == 0b000111000 or b_rep == 0b000011000 or b_rep == 0b000101000:
                        self.eliminate_pointing_row(x, y, num, 1)
                    elif b_rep == 0b000000110 or b_rep == 0b000000111 or b_rep == 0b000000011 or b_rep == 0b000000101:
                        self.eliminate_pointing_row(x, y, num, 2)
                    elif b_rep == 0b100100000 or b_rep == 0b100100100 or b_rep == 0b000100100 or b_rep == 0b100000100:
                        self.eliminate_pointing_col(x, y, num, 0)
                    elif b_rep == 0b010010000 or b_rep == 0b010010010 or b_rep == 0b000010010 or b_rep == 0b010000010:
                        self.eliminate_pointing_col(x, y, num, 1)
                    elif b_rep == 0b001001000 or b_rep == 0b001001001 or b_rep == 0b000001001 or b_rep == 0b001000001:
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

###################################################################################################
###################################################################################################
###################################################################################################

    def solve_box_line_reduction(self):
        candidate_list_copy = self.candidate_list.copy()
        self.solve_box_line_reduction_row()
        self.solve_box_line_reduction_col()
        return not np.array_equal(candidate_list_copy, self.candidate_list)

    def solve_box_line_reduction_row(self):
        for i, row in enumerate(self.candidate_list):
            for num in binary_rep:
                r_reps = 0b0
                for candidate in row:
                    r_reps = r_reps << 1
                    if candidate & num > 0:
                        r_reps = r_reps | 0b1
                if r_reps == 0b110000000 or r_reps == 0b111000000 or r_reps == 0b011000000 or r_reps == 0b101000000:
                    self.eliminate_box_row(i, num, 0)
                elif r_reps == 0b000110000 or r_reps == 0b000111000 or r_reps == 0b000011000 or r_reps == 0b000101000:
                    self.eliminate_box_row(i, num, 1)
                elif r_reps == 0b000000110 or r_reps == 0b000000111 or r_reps == 0b000000011 or r_reps == 0b000000101:
                    self.eliminate_box_row(i, num, 2)
        return

    def eliminate_box_row(self, row_num, candidate, box_y_num):
        sub_row_num = row_num % 3
        avoid_cells = [sub_row_num * 3, sub_row_num * 3 + 1, sub_row_num * 3 + 2]
        x = row_num // 3
        y = box_y_num
        block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

        print("B-R R: Box (" + str(x) + ", " + str(y) + ") sub row " + str(sub_row_num) + " number: " + str(candidate))

        for k, cell in enumerate(block_candidate_list):
            if k not in avoid_cells:
                block_candidate_list[k] = block_candidate_list[k] & (~candidate & 0b111111111)
            self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

    def solve_box_line_reduction_col(self):
        for i, col in enumerate(self.candidate_list.transpose()):
            for num in binary_rep:
                c_reps = 0b0
                for candidate in col:
                    c_reps = c_reps << 1
                    if candidate & num > 0:
                        c_reps = c_reps | 0b1
                if c_reps == 0b110000000 or c_reps == 0b111000000 or c_reps == 0b011000000 or c_reps == 0b101000000:
                    self.eliminate_box_col(i, num, 0)
                elif c_reps == 0b000110000 or c_reps == 0b000111000 or c_reps == 0b000011000 or c_reps == 0b000101000:
                    self.eliminate_box_col(i, num, 1)
                elif c_reps == 0b000000110 or c_reps == 0b000000111 or c_reps == 0b000000011 or c_reps == 0b000000101:
                    self.eliminate_box_col(i, num, 2)
        return

    def eliminate_box_col(self, col_num, candidate, box_x_num):
        sub_col_num = col_num % 3
        avoid_cells = [sub_col_num, sub_col_num + 3, sub_col_num + 6]
        x = box_x_num
        y = col_num // 3
        block_candidate_list = np.reshape(self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3], (1, 9))[0]

        print("B-C R: Box (" + str(x) + ", " + str(y) + ") sub col " + str(sub_col_num) + " number: " + str(candidate))

        for k, cell in enumerate(block_candidate_list):
            if k not in avoid_cells:
                block_candidate_list[k] = block_candidate_list[k] & (~candidate & 0b111111111)
            self.candidate_list[x * 3: x * 3 + 3, y * 3: y * 3 + 3] = np.reshape(block_candidate_list, (3, 3))
        return

###################################################################################################
###################################################################################################
###################################################################################################

    def solve_x_sword_jelly(self):
        candidate_list_copy = self.candidate_list.copy()
        self.solve_x_sword_jelly_row()
        self.solve_x_sword_jelly_col()
        return not np.array_equal(candidate_list_copy, self.candidate_list)

    def solve_x_sword_jelly_row(self):
        for num in binary_rep:
            x_sword_jelly_list = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
            for i, row in enumerate(self.candidate_list):
                base = 0b0
                for j, cell in enumerate(row):
                    base = base << 1
                    if cell & num > 0:
                        base = base | 0b1
                x_sword_jelly_list[i] = base

            non_zeros = np.where(x_sword_jelly_list != 0)[0]

            for hidden_rate in [2, 3, 4]:

                if len(non_zeros) <= hidden_rate:
                    continue

                col_cells = None
                row_cells = None
                for comb in list(combinations(non_zeros, hidden_rate)):
                    base = 0b000000000
                    for row in comb:
                        base = base | x_sword_jelly_list[row]
                    if bin(base).count("1") == hidden_rate:
                        col_cells = base
                        row_cells = comb
                        print("Found X Wing size " + str(hidden_rate) + " for num " + str(num) + " in rows " +
                              str(row_cells) + " in cols " + str(format(base, '09b')))
                        break

                if col_cells is not None and row_cells is not None:
                    for j, col in enumerate(binary_rep):
                        if col & col_cells > 0:
                            for i in range(self.rows):
                                if i not in row_cells:
                                    self.candidate_list[i][j] = self.candidate_list[i][j] & (~num & 0b111111111)

    def solve_x_sword_jelly_col(self):
        for num in binary_rep:
            x_sword_jelly_list = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
            for i, col in enumerate(self.candidate_list.transpose()):
                base = 0b0
                for j, cell in enumerate(col):
                    base = base << 1
                    if cell & num > 0:
                        base = base | 0b1
                x_sword_jelly_list[i] = base

            non_zeros = np.where(x_sword_jelly_list != 0)[0]

            for hidden_rate in [2, 3, 4]:

                if len(non_zeros) <= hidden_rate:
                    continue

                col_cells = None
                row_cells = None
                for comb in list(combinations(non_zeros, hidden_rate)):
                    base = 0b000000000
                    for col in comb:
                        base = base | x_sword_jelly_list[col]
                    if bin(base).count("1") == hidden_rate:
                        row_cells = base
                        col_cells = comb
                        print("Found X Wing size " + str(hidden_rate) + " for num " + str(num) + " in cols " +
                              str(col_cells) + " in rows " + str(format(base, '09b')))
                        break

                if row_cells is not None and col_cells is not None:
                    for i, row in enumerate(binary_rep):
                        if row & row_cells > 0:
                            for j in range(self.cols):
                                if j not in col_cells:
                                    self.candidate_list[i][j] = self.candidate_list[i][j] & (~num & 0b111111111)


###################################################################################################
###################################################################################################
###################################################################################################

    def convert_board_to_string_list(self):

        self.row_list = []
        self.col_list = []
        self.block_list = ["", "", "", "", "", "", "", "", ""]
        self.candidate_string_list = [[""] * 9] * 9

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

        for i in range(9):
            self.candidate_string_list[i] = []
            for j in range(9):
                self.candidate_string_list[i].append(binary_string_to_candidates(self.candidate_list[i][j]))

    def insert_candidate_into_lists(self, x, y, candidate):
        b = 3 * (x // 3) + (y // 3)
        p = (x % 3) * 3 + (y % 3)
        self.row_list[x] = self.row_list[x][:y] + candidate + self.row_list[x][y + 1:]
        self.col_list[y] = self.col_list[y][:x] + candidate + self.col_list[y][x + 1:]
        self.block_list[b] = self.block_list[b][:p] + candidate + self.block_list[b][p + 1:]

    def recursive_has_valid_sudoku_constraints(self, x, y, candidate):

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

    def recursive_is_valid_board(self, x, y, candidate):

        if candidate == -1:
            return True

        if not self.recursive_has_valid_sudoku_constraints(x, y, candidate):
            return False

        self.insert_candidate_into_lists(x, y, candidate)

        return True

    def recursive_solve(self, x, y, candidate):

        if not self.recursive_is_valid_board(x, y, candidate):
            return None

        for i in range(self.rows):
            for j in range(self.cols):

                if self.row_list[i][j] != '0':
                    continue

                for candidate in self.candidate_string_list[i][j]:
                    if self.recursive_solve(i, j, candidate) is not None:
                        return True
                self.insert_candidate_into_lists(i, j, '0')
                return None

        return True

    def solve_sudoku(self):
        start = time.time()
        is_using_recursion = False
        self.get_candidate_list()
        while np.count_nonzero(self.board) < 81:
            if self.solve_naked_singles():
                continue
            elif self.solve_hidden_sets():
                continue
            elif self.solve_pointing_sets():
                continue
            elif self.solve_box_line_reduction():
                continue
            elif self.solve_x_sword_jelly():
                continue
            else:
                is_using_recursion = True
                self.convert_board_to_string_list()
                if self.recursive_solve(0, 0, -1):
                    for i, row in enumerate(self.row_list):
                        for j, value in enumerate(row):
                            self.solution[i][j] = int(value)
                break
        if not is_using_recursion:
            self.solution = self.board.copy()
        if np.count_nonzero(self.solution) < 81:
            return False
        print(time.time() - start)
        return True
