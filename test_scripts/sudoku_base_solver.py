
import time
import numpy as np

rows = 9
bs = 3
blocks_across = int(rows / bs)


def has_valid_sudoku_constraints(board):

    # Checks that the rows are valid
    for i, row in enumerate(board):
        if sum(row > 0) != len(np.unique(row[row > 0])):
            return False

    # Checks that the column are valid
    for i, row in enumerate(board.transpose()):
        if sum(row > 0) != len(np.unique(row[row > 0])):
            return False

    # Checks that the blocks are valid
    for i in range(blocks_across):
        for j in range(blocks_across):
            rearranged = np.resize(board[bs * i:bs * i + 3, bs * j:bs * j + 3], (1, 9))[0]
            if sum(rearranged > 0) != len(np.unique(rearranged[rearranged > 0])):
                return False

    return True


def is_valid_board(board):

    if not has_valid_sudoku_constraints(board):
        return False

    return True


def recursive_solve(board):

    if not is_valid_board(board):
        return None

    for i in range(rows):
        for j in range(rows):

            if board[i, j] != 0:
                continue

            for candidate in range(1, 10):
                board[i, j] = candidate
                if recursive_solve(board) is None:
                    if candidate == 9:
                        board[i, j] = 0
                        return None
                else:
                    return board

    return board


def main():
    board = np.zeros((9, 9))

    # Board ID: 47,641,703
    board[0, :] = [0, 8, 5, 0, 9, 0, 0, 0, 2]
    board[1, :] = [2, 0, 0, 0, 1, 8, 9, 0, 0]
    board[2, :] = [9, 0, 0, 0, 5, 0, 0, 6, 0]
    board[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    board[4, :] = [5, 4, 1, 0, 0, 0, 8, 0, 0]
    board[5, :] = [0, 2, 0, 0, 0, 6, 4, 0, 5]
    board[6, :] = [0, 3, 0, 0, 4, 1, 0, 0, 0]
    board[7, :] = [0, 0, 8, 0, 0, 0, 0, 0, 0]
    board[8, :] = [1, 0, 0, 2, 0, 7, 0, 0, 0]

    print(board)

    start = time.time()
    print(recursive_solve(board))
    print(time.time() - start)


if __name__ == "__main__":
    main()
