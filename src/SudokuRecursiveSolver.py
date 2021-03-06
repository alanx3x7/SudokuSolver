# Introduces heuristic approaches to decrease the number of paths for recursive solving

import time
import numpy as np
from itertools import combinations

# Mapping from binary numbers to decimal numbers
binary_to_real = {
    1: 9,       2: 8,       4: 7,
    8: 6,       16: 5,      32: 4,
    64: 3,      128: 2,     256: 1
}

# List of binary numbers
binary_rep = [0b100000000, 0b010000000, 0b001000000, 0b000100000, 0b000010000, 0b000001000, 0b000000100,
              0b000000010, 0b000000001]


def binary_string_to_candidates(binary):
    """ Converts a binary number to a concatenated string of decimal numbers.
        For example, 0b001011001 becomes '3569'
        :param binary: Binary number [int]
        :return candidates: Concatenated string list [string]
    """
    candidates = ""
    for i, rep in enumerate(binary_rep):
        if binary & rep > 0:
            candidates += str(i + 1)
    return candidates


class SudokuRecursiveSolver:
    """ Class that performs the sudoku solving.
        Currently uses v5 of the sudoku_base_solvers.
        Uses heuristic methods first (with binary representation), then recursion/bifurcation over the remaining
        candidates for each cell (with string representation)
    """

    def __init__(self):
        """ Constructor """

        # Board parameters
        self.rows = 0                           # Number of rows in the board, should be 9
        self.cols = 0                           # Number of cols in the board, should be 9
        self.block_size = 0                     # Size of each block, should be 3 (assumes square blocks)
        self.blocks_across = 0                  # Number of blocks across the board in one direction, should be 3

        # Main containers for the board state
        self.board = None                       # Current board (used as initial and for recursion/bifurcation)
        self.solution = None                    # Solved board state

        # Heuristic approach container
        self.candidate_list = None              # Binary representation of candidates for each cell

        # Recursion/bifurcation approach containers
        self.row_list = None                    # List of cell values for each row in string representation
        self.col_list = None                    # List of cell values for each col in string representation
        self.block_list = None                  # List of block values for each block in string representation
        self.candidate_string_list = None       # List of candidates for each cell in string representation

    def load_board(self, game_board, block_size=3):
        """ Load the sudoku puzzle board and gets the board characteristics
            :param game_board: The sudoku board state, with 0's as blanks [2D list of ints]
            :param block_size: Size of a block, assuming square blocks [int]
            :return: None
        """

        # Set up initial state of board and solution as the game_board
        self.board = np.array(game_board)
        self.solution = self.board.copy()

        # Board should be 2D
        self.rows, self.cols = self.board.shape
        self.block_size = block_size
        self.blocks_across = int(self.rows / self.block_size)

        # Initialize candidate list as empty
        self.candidate_list = np.zeros((self.rows, self.cols), dtype=int)

    def block_top_left(self, x, y):
        """ Returns the (i, j) cell index of the top left cell of block (x, y)
            :param x: The xth block in the vertical direction [int]
            :param y: The yth block in the horizontal direction [int]
            :return top_x: The index of the top left cell in the block in the vertical direction [int]
            :return top_y: THe index of the top left cell in the block in the horizontal direction [int]
        """
        top_x = (x // self.block_size) * self.blocks_across
        top_y = (y // self.block_size) * self.blocks_across
        return top_x, top_y

###################################################################################################
###################################################################################################
###################################################################################################
    """ 
        Set up the board for the heuristic solver for the SudokuSolver.

        Heuristics means that a series of logical deductions are used to figure out which value
        goes into each cell. No guess work is done here, and all of the techniques used are 
        established techniques used to solve sudoku puzzles. In essence, these techniques serve
        to find groups of cells that can only contain a certain subset of values, which in turn
        restricts those values from appearing in other cells that are related.
        
        For the heuristic solver, because we want to be able to find groups of cells that contain
        similar candidates, we opt for a binary representation approach. That is, each value in
        the candidate list corresponds to the possible candidates/values that the cell can take.
        They are represented in the form 0bxxxxxxxxx, where x is 1 if that value is a candidate 
        for this cell, and 0 if that value cannot be a candidate, from 1 to 9 in MSB order.
        
        In other words, say for example cell (1, 3) has candidates 1, 3, 4, 7, 8. Then, in cell
        (1, 3) (which is index (0, 2)) in candidate list is 0b101100110. We see the first, third,
        fourth, seventh, and eighth bits counting from the most significant bit are set to 1.
    """

    def has_valid_sudoku_constraints(self, x, y, candidate):
        """ Checks if this value is a valid candidate for cell (x, y).
            Since this is a naive check, it simply checks whether the value of that candidate already appears
            in a cell in the same row, column, or block as cell (x, y). If such a value exists, it violates
            the sudoku constraints and that value can not be a candidate for this cell.
            :param x: The x coordinate of the cell in question [int]
            :param y: The y coordinate of the cell in question [int]
            :param candidate: The value of the candidate [int]
            :return bool: True if it is a candidate, false if that candidate cannot go there
        """

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
        """ Checks that whether the board will meet sudoku constraints if candidate goes into cell (x, y)
            Currently only checks for normal sudoku constraints. Will be adding knight's move or other constraints
            in the future.
            :param x: The x coordinate of the cell in question [int]
            :param y: The y coordinate of the cell in question [int]
            :param candidate: The value of the candidate [int]
            :return bool: True if sudoku constraints are met when candidate goes into cell (x, y). False otherwise.
        """

        # We ignore if candidate is -1. This is just used for entry into the recursion
        if candidate == -1:
            return True

        # Checks with normal sudoku constraints
        if not self.has_valid_sudoku_constraints(x, y, candidate):
            return False

        return True

    def get_candidate_list(self):
        """ Creates the candidate list for each cell on in the board. If the cell is already filled, the candidate
            list is composed of only 0's.
        """

        # Loops through each cell on the board
        for i in range(self.rows):
            for j in range(self.cols):

                valid_candidates = 0b0

                # We skip this cell if it already has a value
                if self.board[i][j] == 0:

                    # We go through all numbers, and if they yield a valid sudoku puzzle, the candidate list is updated
                    # accordingly (that is, if x put into cell (i, j) gives a valid sudoku, the xth bit of the candidate
                    # list binary number is set to 1. It is set to 0 otherwise.
                    for candidate in range(1, 10):
                        valid_candidates = valid_candidates << 1
                        if self.is_valid_board(i, j, candidate):
                            valid_candidates += 0b1

                # Save the candidates
                self.candidate_list[i][j] = valid_candidates

    """ Heuristic: Naked Singles """

    def solve_naked_singles(self):
        """ Finds all naked singles from the candidate list and update the board and candidate list accordingly
            by placing those values into those cells.
            :return modified_board: True if the board was updated, false otherwise
        """
        modified_board = False

        # Loops through each cell
        for i in range(self.rows):
            for j in range(self.cols):

                # If there is only one possible candidate in that cell
                if bin(self.candidate_list[i][j]).count("1") == 1:

                    # Update the board by placing that value into that cell and update the candidate list
                    self.insert_value_and_update_candidate_list(self.candidate_list[i][j], i, j)
                    modified_board = True

        # Return true if the board was updated, false otherwise.
        return modified_board

    def insert_value_and_update_candidate_list(self, binary_value, x, y):
        """ Inserts value into cell (x, y) in the board and update the candidate list accordingly
            :param binary_value: The value to be inserted into the cell in binary format [int]
            :param x: The x coordinate of the cell to be updated [int]
            :param y: The y coordinate of the cell to be updated [int]
            :return: None
        """

        # Since we want decimal numbers in the board, we find the decimal equivalent to the binary value
        decimal_value = binary_to_real[binary_value]

        # Update the board with this value
        self.board[x][y] = decimal_value

        # Remove this candidate from all other cells that share the same row as cell (x, y)
        for i, candidates in enumerate(self.candidate_list[x, :]):
            self.candidate_list[x, i] = candidates & (~binary_value & 0b111111111)

        # Remove this candidate from all other cells that share the same column as cell (x, y)
        for j, candidates in enumerate(self.candidate_list[:, y]):
            self.candidate_list[j, y] = candidates & (~binary_value & 0b111111111)

        # Remove this candidate from all other cells that share the same block as cell (x, y)
        top_x, top_y = self.block_top_left(x, y)
        for i in range(top_x, top_x + 3):
            for j in range(top_y, top_y + 3):
                self.candidate_list[i, j] = self.candidate_list[i][j] & (~binary_value & 0b111111111)

    """ Heuristic: Hidden Sets """

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
