
import time
import numpy as np

rows = 9
bs = 3
blocks_across = int(rows / bs)


def has_valid_sudoku_constraints(row_list, col_list, block_list, x, y, candidate):

    # Checks that the rows are valid
    if candidate in row_list[x]:
        return False

    # Checks that the column are valid
    if candidate in col_list[y]:
        return False

    # Checks that the blocks are valid
    block_num = 3 * (x // 3) + (y // 3)
    if candidate in block_list[block_num]:
        return False

    return True


def is_valid_board(row_list, col_list, block_list, x, y, candidate):

    if candidate == -1:
        return True

    if not has_valid_sudoku_constraints(row_list, col_list, block_list, x, y, candidate):
        return False

    b = 3 * (x // 3) + (y // 3)
    p = (x % 3) * 3 + (y % 3)
    row_list[x] = row_list[x][:y] + candidate + row_list[x][y + 1:]
    col_list[y] = col_list[y][:x] + candidate + col_list[y][x + 1:]
    block_list[b] = block_list[b][:p] + candidate + block_list[b][p + 1:]

    return True


def recursive_solve(row_list, col_list, block_list, x, y, candidate):

    if not is_valid_board(row_list, col_list, block_list, x, y, candidate):
        return None

    for i in range(rows):
        for j in range(rows):

            if row_list[i][j] != '0':
                continue

            #print("Cell: " + str(i) + ", " + str(j))

            for candidate in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                #print(candidate, end=" ")
                if recursive_solve(row_list, col_list, block_list, i, j, candidate) is not None:
                    return True

            b = 3 * (x // 3) + (y // 3)
            p = (x % 3) * 3 + (y % 3)
            row_list[x] = row_list[x][:y] + '0' + row_list[x][y + 1:]
            col_list[y] = col_list[y][:x] + '0' + col_list[y][x + 1:]
            block_list[b] = block_list[b][:p] + '0' + block_list[b][p + 1:]

            #print()
            return None

    return True


def convert_board_to_string(board):
    row_list = []
    col_list = []
    for i in range(9):
        row = ""
        col = ""
        for j in range(9):
            row += str(int(board[i][j]))
            col += str(int(board[j][i]))
        row_list.append(row)
        col_list.append(col)

    block_list = ["", "", "", "", "", "", "", "", ""]
    for i in range(9):
        for j in range(9):
            block = 3 * (i // 3) + (j // 3)
            block_list[block] += str(int(board[i][j]))

    return row_list, col_list, block_list


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
    # board[0, :] = [3, 0, 0, 0, 0, 0, 0, 0, 6]
    # board[1, :] = [0, 0, 7, 0, 0, 6, 5, 0, 0]
    # board[2, :] = [0, 4, 0, 0, 0, 0, 0, 0, 0]
    # board[3, :] = [0, 0, 0, 1, 5, 0, 0, 0, 0]
    # board[4, :] = [0, 0, 0, 2, 0, 0, 7, 0, 4]
    # board[5, :] = [0, 2, 0, 0, 0, 0, 1, 3, 0]
    # board[6, :] = [0, 9, 0, 0, 8, 7, 0, 6, 2]
    # board[7, :] = [0, 0, 0, 0, 0, 9, 8, 5, 0]
    # board[8, :] = [5, 0, 0, 0, 6, 0, 3, 0, 0]

    print(board)
    start = time.time()
    row_list, col_list, block_list = convert_board_to_string(board)
    print(row_list)
    print(col_list)
    print(block_list)
    recursive_solve(row_list, col_list, block_list, 0, 0, -1)
    print(time.time() - start)
    print(board)
    print(row_list)
    print(col_list)
    print(block_list)

    board = np.zeros((9, 9))
    for i, row in enumerate(row_list):
        for j, value in enumerate(row):
            board[i][j] = int(value)

    print(board)

if __name__ == "__main__":
    main()
