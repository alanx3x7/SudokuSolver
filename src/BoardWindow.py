import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget


class SudokuCell(QWidget):
    """ Class for an individual widget within the sudoku board widget
    """

    def __init__(self, x, y, value):
        """ Constructor
            :param parent: The parent to this widget
        """
        super(SudokuCell, self).__init__()

        # Parameters to hold the characteristics of the cell itself
        self.x = x                          # x coordinate of the cell in the board
        self.y = y                          # y coordinate of the cell in the board
        self.value = value                  # Value to be displayed in this cell
        self.border_colour = Qt.darkGreen   # Border colour for this cell

    def paintEvent(self, event):
        """ Called to draw the cell on the board.
            :param event: Something that triggers the calling of this function
        """

        # Creates the painter object
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        # Set the background to be white and border to be the border colour member variable
        outer, inner = self.border_colour, Qt.white
        pen = QtGui.QPen(outer, 2, Qt.SolidLine)
        p.setPen(pen)
        p.setBrush(QtGui.QBrush(inner, Qt.SolidPattern))
        p.drawRect(r)

        # Get the coordinates of the corners of this cell
        tl_x = r.x()
        tl_y = r.y()
        br_x = r.width()
        br_y = r.height()

        # Draw a thicker border if the cell is on the edge of a sudoku block
        pen = QtGui.QPen(self.border_colour, 7, Qt.SolidLine)
        p.setPen(pen)
        if self.x == 2 or self.x == 5:              # If it is on top of a block edge
            p.drawLine(tl_x, br_y, br_x, br_y)
        if self.x == 3 or self.x == 6:              # If it is under a block edge
            p.drawLine(tl_x, tl_y, br_x, tl_y)
        if self.y == 2 or self.y == 5:              # If it is to the left of a block edge
            p.drawLine(br_x, tl_y, br_x, br_y)
        if self.y == 3 or self.y == 6:              # If it is to the right of a block edge
            p.drawLine(tl_x, tl_y, tl_x, br_y)

        # Write the number into the cell
        number_font = QFont('SansSerif', 16)
        number_font.setWeight(75)
        p.setPen(Qt.black)
        p.setFont(number_font)

        # If the number is 0, then we don't write anything as it is effectively blank
        if self.value != 0:
            p.drawText(r, Qt.AlignCenter, str(self.value))


class BoardWindow(QWidget):
    """ Class for the window that displays the solution to the sudoku puzzle after solve
    """

    def __init__(self, parent=None):
        """ Constructor
            :param parent: The parent to this widget
        """
        super(BoardWindow, self).__init__(parent)

        # Define the grid layout that will contain all of the SudokuCell widgets
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)

        # We default it to be 9x9, will expand in the future
        self.board_x_size = 9
        self.board_y_size = 9
        self.board_colour = Qt.darkGreen

        self.load_board()
        self.setLayout(self.grid)

    def load_board(self):
        """ Fill the grid layout with SudokuCell widgets
            :return: None
        """
        for x in range(self.board_x_size):
            for y in range(self.board_y_size):
                w = SudokuCell(x, y, 0)
                self.grid.addWidget(w, x, y)

    def populate_board(self, grid):
        """ Assign values to each of the SudokuCells in the grid layout
            :param grid: The values for each cell in the grid [2D list of int]
            :return: None
        """

        # For every cell in the grid
        for i, rows in enumerate(grid):
            for j, value in enumerate(rows):

                # Get the widget, update its value and colour
                w = self.grid.itemAtPosition(i, j).widget()
                w.value = value
                w.border_colour = self.board_colour
                w.update()

    def valid_board(self, is_valid):
        """ Assign colour of the displayed board based on the validity of the solution. If valid, the colour of the
            board is dark green. If invalid, the colour of the board is red.
            :param is_valid: Whether the solution to be displayed is valid [bool]
            :return: None
        """
        if is_valid:
            self.board_colour = Qt.darkGreen
        else:
            self.board_colour = Qt.red

    def paintEvent(self, e):
        """ Called to draw the borders to the grid layout in the widget
            :param e: Event handler
            :return: None
        """

        # Creates the paint brush object to draw
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        """ Draws lines around the border of the grid layout to form the border of the sudoku puzzle.
            :param qp: The painter object that does the drawing [QPainter]
            :return: None
        """

        # Get the geometry of this widget and adjust based on margins
        widget_shape = self.geometry()
        top_left_x = widget_shape.x() + 10
        top_left_y = widget_shape.y() + 10
        bottom_right_x = widget_shape.width() - 10
        bottom_right_y = widget_shape.height() - 10

        # Draw the borders to the sudoku board which is the grid layout
        pen = QtGui.QPen(self.board_colour, 5, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(top_left_x, top_left_y, top_left_x, bottom_right_y)
        qp.drawLine(top_left_x, top_left_y, bottom_right_x, top_left_y)
        qp.drawLine(top_left_x, bottom_right_y, bottom_right_x, bottom_right_y)
        qp.drawLine(bottom_right_x, top_left_y, bottom_right_x, bottom_right_y)
