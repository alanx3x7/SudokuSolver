import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from BoardWindow import BoardWindow
from SudokuScreenReader import SudokuScreenReader
from SudokuRecursiveSolver import SudokuRecursiveSolver


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
        self.grid_values = None

        self.setWindowTitle('Sudoku Solver')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowIcon(QtGui.QIcon('../data/sudoku_solver_icon.png'))

        self.screen_capture_enabled = True

        self.initUI()
        self.setLayout(self.main_layout)
        self.show()

    def initUI(self):

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setContentsMargins(10, 10, 10, 10)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.capture_widget = BoardWindow()
        # self.capture_widget = QtWidgets.QWidget()
        self.capture_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addWidget(self.capture_widget)

        self.clear_button = QtWidgets.QPushButton('Clear', self)
        self.button_layout.addWidget(self.clear_button)

        self.solve_button = QtWidgets.QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.button_solve_clicked)
        self.button_layout.addWidget(self.solve_button)

        self.main_layout.addLayout(self.button_layout)

    def updateMask(self):
        # Get the frame and widget geometries
        windowRect = self.geometry()
        captureRect = self.capture_widget.geometry()

        # Define the frame margins based on the frame size of the window
        left = self.frameGeometry().left() - windowRect.left() - 3
        top = self.frameGeometry().top() - windowRect.top() + 8
        right = self.frameGeometry().right() - windowRect.right() + 3
        bottom = self.frameGeometry().bottom() - windowRect.bottom() + 3

        # Centers them about fixed points to align the centers of the window and widget
        windowRect.moveTopLeft(QtCore.QPoint(0, 0))
        captureRect.moveTopLeft(QtCore.QPoint(30, 30))

        # Create the base region mask which includes the frame of the window as well
        region = QtGui.QRegion(windowRect.adjusted(left, top, right, bottom))

        # Subtract the region containing the capture window
        if self.screen_capture_enabled:
            region -= QtGui.QRegion(captureRect)

        self.setMask(region)

    def paintEvent(self, event):
        super(SudokuSolver, self).paintEvent(event)
        if self.dirty:
            self.updateMask()
            self.dirty = False

    def resizeEvent(self, event):
        super(SudokuSolver, self).resizeEvent(event)
        # the first resizeEvent is called before any first-time showEvent and paintEvent
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

        self.grid_values = self.solver.solution
        self.populate_grid()

        self.screen_capture_enabled = False
        self.updateMask()

    def populate_grid(self):

        print(self.grid_values)

        if self.grid_values is not None:
            self.capture_widget.populate_board(self.grid_values)
