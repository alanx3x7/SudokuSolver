
import time
import numpy as np


class SudokuRecursiveSolver:

    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.block_size = 0
        self.blocks_across = 0

        self.board = None
        self.solution = None

    def load_board(self, game_board, block_size=3):
        self.board = np.array(game_board)
        self.solution = self.board.copy()
        self.rows, self.cols = self.board.shape
        self.block_size = block_size
        self.blocks_across = int(self.rows / self.block_size)

    def has_valid_sudoku_constraints(self, x, y, candidate):

        # Checks that the rows are valid
        row = self.solution[x, :]
        if candidate in row:
            return False

        # Checks that the column are valid
        col = self.solution[:, y]
        if candidate in col:
            return False

        # Checks that the blocks are valid
        row_block = (x // 3) * 3
        col_block = (y // 3) * 3
        block = self.solution[row_block:row_block + 3, col_block:col_block + 3]
        if candidate in block:
            return False

        return True

    def is_valid_board(self, x, y, candidate):

        if not self.has_valid_sudoku_constraints(x, y, candidate):
            return False

        self.solution[x, y] = max(candidate, 0)

        return True

    def recursive_solve(self, x, y, candidate):

        if not self.is_valid_board(x, y, candidate):
            return None

        for i in range(self.rows):
            for j in range(self.cols):

                if self.solution[i, j] != 0:
                    continue

                for candidate in range(1, 10):
                    if self.recursive_solve(i, j, candidate) is not None:
                        return True
                self.solution[i, j] = 0
                return None

        return True


def main():
    board = np.zeros((9, 9))

    # Board ID: 3x3 Sudoku Advanced Puzzle ID: 47,641,703
    board[0, :] = [0, 8, 5, 0, 9, 0, 0, 0, 2]
    board[1, :] = [2, 0, 0, 0, 1, 8, 9, 0, 0]
    board[2, :] = [9, 0, 0, 0, 5, 0, 0, 6, 0]
    board[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    board[4, :] = [5, 4, 1, 0, 0, 0, 8, 0, 0]
    board[5, :] = [0, 2, 0, 0, 0, 6, 4, 0, 5]
    board[6, :] = [0, 3, 0, 0, 4, 1, 0, 0, 0]
    board[7, :] = [0, 0, 8, 0, 0, 0, 0, 0, 0]
    board[8, :] = [1, 0, 0, 2, 0, 7, 0, 0, 0]

    # Board ID: 3x3 Sudoku Evil Puzzle ID: 946,151
    # board[0, :] = [0, 0, 0, 3, 0, 0, 0, 0, 0]
    # board[1, :] = [0, 0, 9, 8, 0, 0, 6, 2, 0]
    # board[2, :] = [3, 0, 5, 0, 0, 0, 1, 9, 0]
    # board[3, :] = [0, 0, 0, 0, 6, 8, 0, 0, 1]
    # board[4, :] = [0, 0, 6, 1, 0, 0, 0, 3, 8]
    # board[5, :] = [0, 0, 0, 9, 0, 0, 7, 0, 0]
    # board[6, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # board[7, :] = [0, 1, 0, 0, 2, 0, 5, 7, 0]
    # board[8, :] = [0, 0, 0, 7, 9, 5, 0, 0, 0]

    print(board)
    start = time.time()
    recursive_solve(board, 0, 0, -1)
    print(time.time() - start)
    print(board)


if __name__ == "__main__":
    main()
