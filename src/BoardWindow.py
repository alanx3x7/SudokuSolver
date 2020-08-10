import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget


class SudokuCell(QWidget):

    def __init__(self, x, y, value):
        super(SudokuCell, self).__init__()

        # Sets the default size of the cell
        # self.size = 40
        # self.setFixedSize(QtCore.QSize(self.size, self.size))

        # Parameters to hold the characteristics of the cell itself
        self.x = x  # x coordinate of the cell in the board
        self.y = y  # y coordinate of the cell in the board
        self.value = value

    def paintEvent(self, event):
        """ Called to draw the cell on the board.
        :param event: Something that triggers the calling of this function
        """

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        outer, inner = Qt.black, Qt.white               # We set it to be a white circle with black border
        pen = QtGui.QPen(outer, 1.5, Qt.SolidLine)            # We set border to be a solid line of thickness 1.5
        p.setPen(pen)
        p.setBrush(QtGui.QBrush(inner, Qt.SolidPattern))
        p.drawRect(r)                                # We draw a circle

        number_font = QFont('SansSerif', 16)
        number_font.setWeight(75)
        p.setPen(Qt.black)
        p.setFont(number_font)
        if self.value != 0:
            p.drawText(r, Qt.AlignCenter, str(self.value))


class BoardWindow(QWidget):

    def __init__(self, parent=None):
        super(BoardWindow, self).__init__(parent)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(5)

        self.board_x_size = 9
        self.board_y_size = 9

        self.load_board()

        self.setLayout(self.grid)

    def load_board(self):
        for x in range(self.board_x_size):
            for y in range(self.board_y_size):
                w = SudokuCell(x, y, 0)
                self.grid.addWidget(w, x, y)

    def populate_board(self, grid):

        for i, rows in enumerate(grid):
            for j, value in enumerate(rows):

                print(value)

                if value == 0:
                    continue

                w = self.grid.itemAtPosition(i, j).widget()
                w.value = value
                w.update()
