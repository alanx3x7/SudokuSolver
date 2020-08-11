from SudokuRecursiveSolver import SudokuRecursiveSolver
from SudokuScreenReader import SudokuScreenReader
from SudokuScreenWriter import SudokuScreenWriter

if __name__ == "__main__":
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
