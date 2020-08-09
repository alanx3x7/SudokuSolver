import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from SudokuRecursiveSolver import SudokuRecursiveSolver
from SudokuScreenReader import SudokuScreenReader


class SudokuSolver(QWidget):

    dirty = True

    def __init__(self, parent=None):
        super(SudokuSolver, self).__init__(parent)

        self.reader = SudokuScreenReader()
        self.solver = SudokuRecursiveSolver()

        self.capture_widget = None
        self.solve_button = None
        self.clear_button = None
        self.button_layout = None
        self.main_layout = None

        self.setWindowTitle('Icon')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Icon')
        self.initUI()
        self.setLayout(self.main_layout)
        self.show()

    def initUI(self):

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setContentsMargins(10, 10, 10, 10)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.capture_widget = QtWidgets.QWidget()
        self.capture_widget.setAutoFillBackground(True)
        wer = self.capture_widget.palette()
        wer.setColor(self.capture_widget.backgroundRole(), Qt.red)
        self.capture_widget.setPalette(wer)
        self.capture_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addWidget(self.capture_widget)

        self.clear_button = QtWidgets.QPushButton('Clear', self)
        self.button_layout.addWidget(self.clear_button)

        self.solve_button = QtWidgets.QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.button_solve_clicked)
        self.button_layout.addWidget(self.solve_button)

        self.main_layout.addLayout(self.button_layout)

    def updateMask(self):
        # get the *whole* window geometry, including its title bar and borders

        frameRect = self.geometry()  # self.frameGeometry()
        grabGeometry = self.capture_widget.geometry()

        left = -(frameRect.left() - self.frameGeometry().left()) - 3
        top = -(frameRect.top() - self.frameGeometry().top()) + 8
        right = -(frameRect.right() - self.frameGeometry().right()) + 3
        bottom = -(frameRect.bottom() - self.frameGeometry().bottom()) + 3

        # get the capture_widget geometry and remap it to global coordinates
        grabGeometry.moveTopLeft(self.capture_widget.mapToGlobal(QtCore.QPoint(0, 0)))

        # reset the geometries to get "0-point" rectangles for the mask
        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(30, 30))

        # create the base mask region, adjusted to the margins between the
        # grabWidget and the window as computed above
        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))

        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QtGui.QRegion(grabGeometry)

        self.setMask(region)
        # self.setMask(QtGui.QRegion(self.rect()))
        # self.show()
        # self.clearMask()

    def paintEvent(self, event):
        super(SudokuSolver, self).paintEvent(event)
        if self.dirty:
            self.updateMask()
            self.dirty = False

    def resizeEvent(self, event):
        super(SudokuSolver, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            self.updateMask()

    def button_solve_clicked(self):
        grabGeometry = self.capture_widget.geometry()
        grabGeometry.moveTopLeft(self.capture_widget.mapToGlobal(QtCore.QPoint(0, 0)))
        x = grabGeometry.left()
        y = grabGeometry.top()
        w = grabGeometry.width()
        h = grabGeometry.height()

        print("Reading board!")
        self.reader.get_sudoku_board(x, y, w, h)
        self.solver.load_board(self.reader.game_board)
        print(self.solver.board)
        print("Solving board!")
        self.solver.recursive_solve(0, 0, -1)
        print(self.solver.solution)
