from SudokuRecursiveSolver import SudokuRecursiveSolver
from SudokuScreenReader import SudokuScreenReader

if __name__ == "__main__":
    reader = SudokuScreenReader()
    reader.get_sudoku_board(220, 320, 450, 450)

    solver = SudokuRecursiveSolver()
    solver.load_board(reader.game_board)
    print(solver.board)
    solver.recursive_solve(0, 0, -1)
    print(solver.solution)
