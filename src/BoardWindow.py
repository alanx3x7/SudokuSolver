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

        # Parameters to hold the characteristics of the cell itself
        self.x = x  # x coordinate of the cell in the board
        self.y = y  # y coordinate of the cell in the board
        self.value = value
        self.border_colour = Qt.darkGreen

    def paintEvent(self, event):
        """ Called to draw the cell on the board.
        :param event: Something that triggers the calling of this function
        """

        # Creates the painter object and does things to it
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        outer, inner = self.border_colour, Qt.white
        pen = QtGui.QPen(outer, 2, Qt.SolidLine)
        p.setPen(pen)
        p.setBrush(QtGui.QBrush(inner, Qt.SolidPattern))
        p.drawRect(r)

        tl_x = r.x()
        tl_y = r.y()
        br_x = r.width()
        br_y = r.height()

        pen = QtGui.QPen(self.border_colour, 7, Qt.SolidLine)
        p.setPen(pen)
        if self.x == 2 or self.x == 5:
            p.drawLine(tl_x, br_y, br_x, br_y)
        if self.x == 3 or self.x == 6:
            p.drawLine(tl_x, tl_y, br_x, tl_y)
        if self.y == 2 or self.y == 5:
            p.drawLine(br_x, tl_y, br_x, br_y)
        if self.y == 3 or self.y == 6:
            p.drawLine(tl_x, tl_y, tl_x, br_y)

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
        self.grid.setSpacing(0)

        self.board_x_size = 9
        self.board_y_size = 9
        self.board_colour = Qt.darkGreen

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

                w = self.grid.itemAtPosition(i, j).widget()
                w.value = value
                w.border_colour = self.board_colour
                w.update()

    def valid_board(self, is_valid):
        if is_valid:
            self.board_colour = Qt.darkGreen
        else:
            self.board_colour = Qt.red

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        widget_shape = self.geometry()
        top_left_x = widget_shape.x() + 10
        top_left_y = widget_shape.y() + 10
        bottom_right_x = widget_shape.width() - 10
        bottom_right_y = widget_shape.height() - 10

        pen = QtGui.QPen(self.board_colour, 5, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(top_left_x, top_left_y, top_left_x, bottom_right_y)
        qp.drawLine(top_left_x, top_left_y, bottom_right_x, top_left_y)
        qp.drawLine(top_left_x, bottom_right_y, bottom_right_x, bottom_right_y)
        qp.drawLine(bottom_right_x, top_left_y, bottom_right_x, bottom_right_y)
