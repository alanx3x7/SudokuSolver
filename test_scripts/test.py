from SudokuRecursiveSolver import SudokuRecursiveSolver
from SudokuScreenReader import SudokuScreenReader
from SudokuScreenWriter import SudokuScreenWriter
from sudoku_boards import board

from sudoku_base_solver_v3 import SudokuRecursiveSolver3
from sudoku_base_solver_v4 import SudokuRecursiveSolver4
from sudoku_base_solver_v5 import SudokuRecursiveSolver5

import time


def test_with_screen():
    reader = SudokuScreenReader()
    reader.get_sudoku_board(220, 320, 450, 450)

    print(reader.game_board)

    solver = SudokuRecursiveSolver()
    solver.load_board(reader.game_board)
    print(solver.board)
    solver.solve_sudoku()
    print(solver.solution)

    writer = SudokuScreenWriter()
    writer.load_solution_board(220, 320, solver.solution, reader.game_board_contours)
    writer.find_game_board_centers()
    writer.write_in_sudoku()


def test_with_board():
    solver = SudokuRecursiveSolver3()
    for i in range(6):
        start = time.time()
        solver.load_board(board[i])
        solver.solve_sudoku()
        print(time.time() - start)
        print(solver.solution)


if __name__ == "__main__":
    solver = SudokuRecursiveSolver5()
    solver.load_board(board[0])
    solver.get_candidate_list()
    solver.solve_naked_singles()
    print(solver.candidate_list)
    print("Hidden sets 1")
    print(solver.solve_hidden_sets())
    print(solver.candidate_list)
    print("Naked singles 2")
    print(solver.solve_naked_singles())
    print("Hidden sets 2")
    print(solver.solve_hidden_sets())
    print("Pointing pairs 1")
    print(solver.solve_pointing_sets())
    print(solver.candidate_list)
    print("Naked singles 3")
    print(solver.solve_naked_singles())
    print("Hidden sets 3")
    print(solver.solve_hidden_sets())
    print("Pointing pairs 2")
    print(solver.solve_pointing_sets())
    print("Box lines 1")
    print(solver.solve_box_line_reduction())
    print(solver.candidate_list)
    print("Xswordjelly 1")
    print(solver.solve_x_sword_jelly())
    print(solver.candidate_list)
    print("Xswordjelly 2")
    print(solver.solve_x_sword_jelly())
    print(solver.candidate_list)
    solver.solve_hidden_sets()
    solver.solve_naked_singles()
    while solver.solve_hidden_sets():
        solver.solve_naked_singles()

    print(solver.board)

