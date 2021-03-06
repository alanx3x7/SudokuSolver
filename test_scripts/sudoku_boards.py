import numpy as np

board = []

# Board ID: Sudoku Solver X-Wing Example 1
board0 = np.zeros((9, 9))
board0[0, :] = [1, 0, 0, 0, 0, 0, 5, 6, 9]
board0[1, :] = [4, 9, 2, 0, 5, 6, 1, 0, 8]
board0[2, :] = [0, 5, 6, 1, 0, 9, 2, 4, 0]
board0[3, :] = [0, 0, 9, 6, 4, 0, 8, 0, 1]
board0[4, :] = [0, 6, 4, 0, 1, 0, 0, 0, 0]
board0[5, :] = [2, 1, 8, 0, 3, 5, 6, 0, 4]
board0[6, :] = [0, 4, 0, 5, 0, 0, 0, 1, 6]
board0[7, :] = [9, 0, 5, 0, 6, 1, 4, 0, 2]
board0[8, :] = [6, 2, 1, 0, 0, 0, 0, 0, 5]
board.append(board0)


# Board ID: 3x3 Sudoku Advanced Puzzle ID: 47,641,703
board1 = np.zeros((9, 9))
board1[0, :] = [0, 8, 5, 0, 9, 0, 0, 0, 2]
board1[1, :] = [2, 0, 0, 0, 1, 8, 9, 0, 0]
board1[2, :] = [9, 0, 0, 0, 5, 0, 0, 6, 0]
board1[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 1]
board1[4, :] = [5, 4, 1, 0, 0, 0, 8, 0, 0]
board1[5, :] = [0, 2, 0, 0, 0, 6, 4, 0, 5]
board1[6, :] = [0, 3, 0, 0, 4, 1, 0, 0, 0]
board1[7, :] = [0, 0, 8, 0, 0, 0, 0, 0, 0]
board1[8, :] = [1, 0, 0, 2, 0, 7, 0, 0, 0]
board.append(board1)

# Board ID: 3x3 Sudoku Evil Puzzle ID: 946,151
board2 = np.zeros((9, 9))
board2[0, :] = [0, 0, 0, 3, 0, 0, 0, 0, 0]
board2[1, :] = [0, 0, 9, 8, 0, 0, 6, 2, 0]
board2[2, :] = [3, 0, 5, 0, 0, 0, 1, 9, 0]
board2[3, :] = [0, 0, 0, 0, 6, 8, 0, 0, 1]
board2[4, :] = [0, 0, 6, 1, 0, 0, 0, 3, 8]
board2[5, :] = [0, 0, 0, 9, 0, 0, 7, 0, 0]
board2[6, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
board2[7, :] = [0, 1, 0, 0, 2, 0, 5, 7, 0]
board2[8, :] = [0, 0, 0, 7, 9, 5, 0, 0, 0]
board.append(board2)

# Board ID: 3x3 Sudoku Advanced Puzzle ID: 47,641,703
board3 = np.zeros((9, 9))
board3[0, :] = [3, 0, 0, 0, 0, 0, 0, 0, 6]
board3[1, :] = [0, 0, 7, 0, 0, 6, 5, 0, 0]
board3[2, :] = [0, 4, 0, 0, 0, 0, 0, 0, 0]
board3[3, :] = [0, 0, 0, 1, 5, 0, 0, 0, 0]
board3[4, :] = [0, 0, 0, 2, 0, 0, 7, 0, 4]
board3[5, :] = [0, 2, 0, 0, 0, 0, 1, 3, 0]
board3[6, :] = [0, 9, 0, 0, 8, 7, 0, 6, 2]
board3[7, :] = [0, 0, 0, 0, 0, 9, 8, 5, 0]
board3[8, :] = [5, 0, 0, 0, 6, 0, 3, 0, 0]
board.append(board3)

# Board ID: 3x3 Sudoku Evil Puzzle ID: 10,137,633
board4 = np.zeros((9, 9))
board4[0, :] = [0, 1, 0, 9, 0, 4, 0, 0, 6]
board4[1, :] = [6, 0, 0, 0, 3, 0, 0, 5, 0]
board4[2, :] = [0, 0, 2, 6, 0, 0, 4, 0, 0]
board4[3, :] = [1, 0, 8, 0, 0, 7, 0, 0, 4]
board4[4, :] = [0, 7, 0, 0, 0, 0, 0, 8, 0]
board4[5, :] = [3, 0, 0, 8, 0, 0, 5, 0, 7]
board4[6, :] = [0, 0, 9, 0, 0, 8, 1, 0, 0]
board4[7, :] = [0, 6, 0, 0, 1, 0, 0, 0, 8]
board4[8, :] = [8, 0, 0, 3, 0, 6, 0, 4, 0]
board.append(board4)

# Board ID: 3x3 Sudoku Evil Puzzle ID: 415,452
board5 = np.zeros((9, 9))
board5[0, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
board5[1, :] = [5, 0, 2, 0, 0, 0, 0, 4, 0]
board5[2, :] = [4, 8, 0, 0, 5, 9, 0, 6, 0]
board5[3, :] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
board5[4, :] = [0, 7, 9, 6, 0, 0, 0, 0, 0]
board5[5, :] = [3, 2, 0, 0, 1, 0, 7, 0, 0]
board5[6, :] = [1, 0, 4, 0, 9, 6, 0, 0, 8]
board5[7, :] = [0, 0, 7, 8, 0, 0, 0, 2, 1]
board5[8, :] = [0, 0, 0, 4, 0, 0, 0, 3, 0]
board.append(board5)

# Board ID: 3x3 Sudoku Evil Puzzle ID: 7,442,005
board6 = np.zeros((9, 9))
board6[0, :] = [0, 3, 0, 0, 0, 0, 0, 5, 0]
board6[1, :] = [0, 0, 0, 5, 3, 8, 0, 0, 0]
board6[2, :] = [0, 0, 6, 0, 0, 0, 4, 0, 0]
board6[3, :] = [9, 2, 0, 7, 0, 5, 0, 4, 3]
board6[4, :] = [0, 1, 0, 0, 0, 0, 0, 2, 0]
board6[5, :] = [6, 0, 0, 0, 0, 0, 0, 0, 1]
board6[6, :] = [1, 0, 0, 4, 0, 9, 0, 0, 2]
board6[7, :] = [0, 6, 0, 0, 0, 0, 0, 7, 0]
board6[8, :] = [0, 5, 0, 1, 0, 7, 0, 8, 0]
board.append(board6)

# Board ID: Sudoku Solver Pointing Pairs Example 1
board7 = np.zeros((9, 9))
board7[0, :] = [0, 1, 7, 9, 0, 3, 6, 0, 0]
board7[1, :] = [0, 0, 0, 0, 8, 0, 0, 0, 0]
board7[2, :] = [9, 0, 0, 0, 0, 0, 5, 0, 7]
board7[3, :] = [0, 7, 2, 0, 1, 0, 4, 3, 0]
board7[4, :] = [0, 0, 0, 4, 0, 2, 0, 7, 0]
board7[5, :] = [0, 6, 4, 3, 7, 0, 2, 5, 0]
board7[6, :] = [7, 0, 1, 0, 0, 0, 0, 6, 5]
board7[7, :] = [0, 0, 0, 0, 3, 0, 0, 0, 0]
board7[8, :] = [0, 0, 5, 6, 0, 1, 7, 2, 0]
board.append(board7)

# Board ID: Sudoku Solver Box-Line Reduction Example 1
board8 = np.zeros((9, 9))
board8[0, :] = [0, 1, 6, 0, 0, 7, 8, 0, 3]
board8[1, :] = [0, 9, 0, 8, 0, 0, 0, 0, 0]
board8[2, :] = [8, 7, 0, 0, 0, 1, 2, 6, 0]
board8[3, :] = [0, 4, 8, 0, 0, 0, 3, 0, 0]
board8[4, :] = [6, 5, 0, 0, 0, 9, 0, 8, 2]
board8[5, :] = [0, 3, 9, 0, 0, 0, 6, 5, 0]
board8[6, :] = [0, 6, 0, 9, 0, 0, 0, 2, 0]
board8[7, :] = [0, 8, 0, 0, 0, 2, 9, 3, 6]
board8[8, :] = [9, 2, 4, 6, 0, 0, 5, 1, 0]
board.append(board8)
