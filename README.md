# Sudoku Solver

<img align="right" src=data/SudokuSolverReadMe_Valid_Board.gif width="396" height="362"/>

<p align="justify">
The Sudoku Solver is a Python GUI App that automatically reads the contents of a sudoku on the screen of the user,
and solves that sudoku using a mixture of both heuristic approaches and recursive bifurcations. 

To use, drag the GUI
over the sudoku you want to solve on the screen of your device, and resize the GUI such that the sudoku fits perfectly 
inside the window of the GUI. Ensure that there aren't any numbers outside of the sudoku puzzle that appear in the 
window. Then, press the 'Solve' button. The app will take a few seconds to read the sudoku board within its window,
and once read, it will automatically compute the solution to the sudoku board, if it exists. 

If the sudoku puzzle
has a valid solution and the app has found it, the 'Fill' will become active. Pressing 'Fill' will then allow the GUI
to automatically fill in the sudoku on screen. Press 'Clear' anytime to reset the app and allow capture and solve of
another sudoku puzzle.
</p>



___
### Demo

<img align="left" src=data/SudokuSolverReadMe_Fill_Board.gif width="324" height="297"/>
<p align="justify">
If a valid solution has been found, then the Sudoku puzzle shown in the GUI will have a green border. Once the solution
is displayed, the 'Fill' button will also be activated. When clicked on, the 'Fill' button will automatically take 
control of the mouse and keyboard of the device, and start entering the digits of the solution into the sudoku puzzle
on screen. For this to work, ensure that the sudoku puzzle on screen can be filled by mouse clicks to select each cell
and keyboard presses of the relevant number. Ensure that the positioning of the sudoku puzzle on screen does not change
in between pressing the 'Solve' button and the 'Fill' button, as the app remembers the location of the sudoku puzzle on
screen when the sudoku puzzle is read. The GUI itself can be moved around, however.
</p>



<img align="left" src=data/SudokuSolverReadMe_Invalid_Board.gif width="324" height="297"/>
<p align="justify">
If an invalid sudoku board is read in, then the solver will be unable to find a solution. This will cause it to display
the sudoku puzzle that was read in, with a red border, to indicate invalidity. The 'Fill' button is disabled in this
case. This may happen if the sudoku puzzle read in is invalid, there are mistakes in the sudoku puzzle, other numbers
from outside of the sudoku puzzle are read in, or the OCR (optical character recognition) incorrectly recognizes a 
digit in the puzzle. If numbers outside of the sudoku puzzle are read in, please resize the GUI window such that it
includes only the sudoku puzzle. If the OCR incorrectly reads a digit, try resizing the sudoku puzzle on screen and the
GUI corresponding. If that doesn't help, please let me know - the OCR isn't the greatest here, and I have a running
dictionary of common mis-recognitions that I use to replace instances where the OCR doesn't recognize the digit
correctly.
</p>

___
### Theory


___
### Dependencies and Installation
- Install tesseract [here](https://github.com/UB-Mannheim/tesseract/wiki) (for OCR)
- OpenCV
- PyQT5
- Numpy
- PyInstaller
- PyAutoGUI
- PyTesseract
- Imutils

___
### Future Work
- Currently only solves normal 3x3 sudoku boards, hence will be trying to add functionality that helps solves puzzles
with a knight's move constraint and a king's move constraint
- Improvement on the screen reading speed by exploring other OCRs

___
### Bugs List
- Stop crashing when reading invalid board
- Detect an invalid board when reading in
___
### Credits and Resources
- PyQT Examples [here](https://github.com/pyqt/examples), [here](https://wiki.python.org/moin/PyQt/Tutorials), and [here](http://zetcode.com/gui/pyqt5/firstprograms/)
- [PyAutoGUI help with masking widgets](https://stackoverflow.com/questions/57717331/is-it-possible-to-create-qmainwindow-with-only-outer-border)
- [PyAutoGUI adjusting transparency of QWindow](https://www.geeksforgeeks.org/pyqt5-how-to-create-semi-transparent-window/#:~:text=When%20we%20design%20an%20application,belongs%20to%20the%20QWidget%20class%20.)
- [Reading and parsing squares in sudoku](https://stackoverflow.com/questions/59182827/how-to-get-the-cells-of-a-sudoku-grid-with-opencv)
- [Sudoku puzzle website](https://www.puzzle-sudoku.com/)
- [Sudoku techniques website](https://www.sudokuwiki.org/sudoku.htm)