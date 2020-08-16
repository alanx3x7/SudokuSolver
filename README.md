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

<br />

___
### Demo


<img align="left" src=data/SudokuSolverReadMe_Fill_Board.gif width="324" height="297"/>
<br />
<p align="justify">
If a valid solution has been found, then the Sudoku puzzle shown in the GUI will have a green border. Once the solution
is displayed, the 'Fill' button will also be activated. When clicked on, the 'Fill' button will automatically take 
control of the mouse and keyboard of the device, and start entering the digits of the solution into the sudoku puzzle
on screen. For this to work, ensure that the sudoku puzzle on screen can be filled by mouse clicks to select each cell
and keyboard presses of the relevant number. Ensure that the positioning of the sudoku puzzle on screen does not change
in between pressing the 'Solve' button and the 'Fill' button, as the app remembers the location of the sudoku puzzle on
screen when the sudoku puzzle is read. The GUI itself can be moved around, however.
</p>

<br />
<br />
<img align="left" src=data/SudokuSolverReadMe_Invalid_Board.gif width="324" height="297"/>
<p align="justify">
If an invalid sudoku board is read in, then the solver will be unable to find a solution. This will cause it to display
the sudoku puzzle that was read in, with a red border. The 'Fill' button is disabled in this case. This may happen if 
the sudoku puzzle has are mistakes, other numbers from outside of the sudoku puzzle are read in, or the OCR incorrectly 
reads a digit in the puzzle. If numbers outside of the sudoku puzzle are read in, please resize the GUI window such that 
it includes only the sudoku puzzle. If the OCR incorrectly reads a digit, try resizing the sudoku puzzle on screen and 
the GUI corresponding. If that doesn't help, please let me know - the OCR isn't the greatest, and I have a dictionary of 
common mis-recognitions that I use to replace instances where the OCR doesn't recognize the digit correctly.
</p>

<br />

___
### Theory

#### SudokuScreenReader
<p align="justify">
The SudokuScreenReader class is responsible for reading the contents of the screen that the window of the GUI is placed
over. It first grabs the screen contents corresponding to that area via PyAutoGUI, which is able to take a screenshot
of a certain area of the screen. Subsequently, OpenCV is used to perform a series of filtering and contour finding in 
order to obtain the location of the lines in the sudoku grid. Using those lines, each cell is extracted from the grid.
Each of these cells is then passed to an optical character recognition library (OCR) called PyTesseract, which is a 
wrapper library around Tesseract, an OCR Library. The library is then able to read the character in each cell 
individually. These contents are then sorted by location, which yields our sudoku board. 


For OpenCV processing, the image taken was first thresholded using an adaptive threshold in order to obtain a binary
image. Contours when then found using OpenCV's FindContours. This allowed the grid lines of the puzzle to be found. 
Once the contours corresponding to the grid lines were found, the contents inside each contour was removed, causing 
only the grid lines to remain. These remaining grid lines were then put through morphological operations to straighten
them. Once straightened, the contours were then re-found. These contours were then filtered by size and position, and
the part of the image corresponding to each contour is then provided to the OCR, which reads the digit within that
contour. 

</p>

#### SudokuRecursiveSolver
<p align="justify">
The SudokuRecursiveSolver class is responsible for solving the sudoku board that was read in by the SudokuScreenReader. This 
iteration of the solver uses a combined approach of both heuristics and recursion/bifurcation. Heuristic approaches
include finding naked singles, hidden pairs/triples/sets, pointing pairs, box-line reduction, and also X-wing/swordfish/
jellyfish configurations. For more information about these heuristic approaches, please see the credited sudoku 
techniques website below. Each sudoku is first put through the heuristic approach, and if the solution cannot be found
from those heuristic approaches, recursion/bifurcation is then used. This involves brute-force guessing of all 
remaining possibilities after heuristic approaches have been used. A combined approach was used as heuristic approaches
allowed for a more efficient path of finding the solution and is able to greatly narrow down the solution space. On the
other hand, recursion/bifurcation allows an exhaustive search of the solution space. Therefore, combined we are able to
both minimize the time taken to solve and to maximize the chance of finding the valid solution to the sudoku puzzle.


Multiple approaches to creating a SudokuRecursiveSolver was made. Below are summary statistics of different approaches.
- SudokuSolverV1: Recursion/bifurcation approach. At each step, check every cell to make sure that the sudoku is valid
- SudokuSolverV2: Recursion/bifurcation approach. At each step, check only the row, column, and the block of the current
cell to be guessed for validity instead of the entire board.
- SudokuSolverV3: Recursion/bifurcation approach of V2, except using a string representative of the board instead of
using numpy arrays for much faster comparisons.
- SudokuSolverV4: Recursion/bifurcation approach of V3 with string representation. However, has a priority order of
which cells to initiate guessing with (starts guessing from cells with most to least number of neighbours)
- SudokuSolverV5: Heuristic approaches first, then recursion/bifurcation by going through all candidates in the
 candidate list created by the heuristic approach if solution cannot be found. For the recursion/bifurcation approach,
 the string representation of V3 is used. For heuristic solving, a binary representation is used, to aid in set unions
 and set comparisons needed.

Times are average of 10 successive solves for each board. Times are in seconds. For boards configurations
please see [here](test_scripts/sudoku_boards.py). The current GUI implementation uses V5.

|Board Number|V1|V2|V3|V4|V5|
|---|---|---|---|---|---|
|Board 0|-|-|0.009956|3.200806|0.018799|
|Board 1|-|-|0.076237|DNF|0.020604|
|Board 2|-|-|0.115005|DNF|0.016700|
|Board 3|-|-|14.90483|DNF|0.020199|
|Board 4|-|-|0.141702|DNF|0.074500|
|Board 5|-|-|5.169844|DNF|0.007699|
|Board 6|-|-|0.036300|DNF|0.040399|
|Board 7|-|-|0.037196|DNF|0.054200|
|Board 8|-|-|0.027304|DNF|0.052696|
</p>

#### SudokuScreenWriter
<p align="justify">
The SudokuScreenWriter class is responsible for taking control of the mouse and keyboard of the device and enter in 
the digits of the solved sudoku into the sudoku puzzle on screen. This is done via PyAutoGUI, which is capable of 
controlling the mouse and the keyboard of the device. The position of the cells on the screen is obtained from the 
coordinates of the window when the screenshot of the sudoku board was taken when reading in the digits, and the 
individual cell locations are from the FindContours portion of the SudokuScreenReader. Using these two pieces of 
information, we are able to locate the position of each cell on the screen. The mouse is directed to each cell, filled
and unfilled, clicks on that location, and then the keyboard is pressed to enter the corresponding digit automatically.

This only works if the sudoku screen on board is writable, and that it can be written by clicking on a cell and typing
in the digit into that cell. If the sudoku puzzle is moved on the screen, then the GUI is unable to know where the 
puzzle is located, and will attempt to enter the sudoku puzzle in the location where the screenshot was taken. However,
since this position is independent of the GUI position, the GUI can be moved around before the 'Fill' button operation
takes place.
</p>

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
- Disable screen writing when the user presses a key

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