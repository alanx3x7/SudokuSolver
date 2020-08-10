
import time
import numpy as np

rows = 9
bs = 3
blocks_across = int(rows / bs)


def has_valid_sudoku_constraints(board, x, y, candidate):

    # Checks that the rows are valid
    row = board[x, :]
    if candidate in row:
        return False

    # Checks that the column are valid
    col = board[:, y]
    if candidate in col:
        return False

    # Checks that the blocks are valid
    row_block = (x // 3) * 3
    col_block = (y // 3) * 3
    block = board[row_block:row_block + 3, col_block:col_block + 3]
    if candidate in block:
        return False

    return True


def is_valid_board(board, x, y, candidate):

    if candidate == -1:
        return True

    if not has_valid_sudoku_constraints(board, x, y, candidate):
        return False

    board[x, y] = candidate

    return True


def recursive_solve(board, x, y, candidate):

    if not is_valid_board(board, x, y, candidate):
        return None

    for i in range(rows):
        for j in range(rows):

            if board[i, j] != 0:
                continue

            #print("Cell: " + str(i) + ", " + str(j))

            for candidate in range(1, 10):
                #print(candidate, end=" ")
                if recursive_solve(board, i, j, candidate) is not None:
                    return True
            board[i, j] = 0

            #print()
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

    # Board ID: 3x3 Sudoku Advanced Puzzle ID: 47,641,703
    board[0, :] = [3, 0, 0, 0, 0, 0, 0, 0, 6]
    board[1, :] = [0, 0, 7, 0, 0, 6, 5, 0, 0]
    board[2, :] = [0, 4, 0, 0, 0, 0, 0, 0, 0]
    board[3, :] = [0, 0, 0, 1, 5, 0, 0, 0, 0]
    board[4, :] = [0, 0, 0, 2, 0, 0, 7, 0, 4]
    board[5, :] = [0, 2, 0, 0, 0, 0, 1, 3, 0]
    board[6, :] = [0, 9, 0, 0, 8, 7, 0, 6, 2]
    board[7, :] = [0, 0, 0, 0, 0, 9, 8, 5, 0]
    board[8, :] = [5, 0, 0, 0, 6, 0, 3, 0, 0]

    print(board)
    start = time.time()
    recursive_solve(board, 0, 0, -1)
    print(time.time() - start)
    print(board)


if __name__ == "__main__":
    main()
