import sys
import numpy as np
import pyautogui
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from BoardWindow import BoardWindow
from SudokuScreenReader import SudokuScreenReader
from SudokuScreenWriter import SudokuScreenWriter
from SudokuRecursiveSolver import SudokuRecursiveSolver


class SudokuSolver(QWidget):

    dirty = True

    def __init__(self, parent=None):
        super(SudokuSolver, self).__init__(parent)

        self.reader = SudokuScreenReader()
        self.writer = SudokuScreenWriter()
        self.solver = SudokuRecursiveSolver()

        self.status_text = None
        self.capture_widget = None
        self.solve_button = None
        self.clear_button = None
        self.fill_button = None
        self.button_layout = None
        self.main_layout = None
        self.grid_values = None
        self.sudoku_image = None
        self.main_stack = None
        self.loading_label = None

        self.setWindowTitle('Sudoku Solver')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowIcon(QtGui.QIcon('../data/sudoku_solver_icon.png'))
        self.stack_layer = 0
        self.image_corner_x = None
        self.image_corner_y = None

        self.screen_capture_enabled = True

        self.initUI()
        self.setLayout(self.main_layout)

        self.show()

    def initUI(self):

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setContentsMargins(10, 5, 10, 5)
        self.button_layout = QtWidgets.QHBoxLayout()

        self.status_text = QtWidgets.QLabel()
        self.status_text.setText('Please position window over sudoku on screen!')
        self.status_text.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.main_layout.addWidget(self.status_text)

        self.main_stack = QtWidgets.QStackedWidget(self)

        self.capture_widget = BoardWindow()
        self.capture_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.sudoku_image = QtWidgets.QLabel(self)
        self.main_stack.addWidget(self.capture_widget)
        self.main_stack.addWidget(self.sudoku_image)
        self.main_stack.setCurrentIndex(self.stack_layer)
        self.main_layout.addWidget(self.main_stack)

        self.clear_button = QtWidgets.QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.button_clear_clicked)
        self.clear_button.setEnabled(True)
        self.button_layout.addWidget(self.clear_button)

        self.solve_button = QtWidgets.QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.button_solve_clicked)
        self.solve_button.setEnabled(True)
        self.button_layout.addWidget(self.solve_button)

        self.fill_button = QtWidgets.QPushButton('Fill', self)
        self.fill_button.clicked.connect(self.button_fill_clicked)
        self.fill_button.setEnabled(False)
        self.button_layout.addWidget(self.fill_button)

        self.loading_label = QtWidgets.QLabel(self)
        self.loading_label.setText('Reading numbers from image...')
        self.loading_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.main_layout.addLayout(self.button_layout)

    def updateMask(self):
        # Get the frame and widget geometries
        windowRect = self.geometry()
        captureRect = self.main_stack.geometry()

        # Define the frame margins based on the frame size of the window
        left = self.frameGeometry().left() - windowRect.left() - 3
        top = self.frameGeometry().top() - windowRect.top() + 8
        right = self.frameGeometry().right() - windowRect.right() + 3
        bottom = self.frameGeometry().bottom() - windowRect.bottom() + 3

        # Centers them about fixed points to align the centers of the window and widget
        windowRect.moveTopLeft(QtCore.QPoint(0, 0))
        captureRect.moveTopLeft(QtCore.QPoint(captureRect.left(), captureRect.top()))

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

        center = self.capture_widget.geometry().center()
        self.loading_label.setGeometry(center.x() - 80, center.y(), 230, 40)

        if not self.dirty:
            self.updateMask()

    def display_loading_screen(self, x, y, w, h):

        # Take a screenshot of what's in the window, and convert it to an OpenCV Image
        im1 = pyautogui.screenshot(region=(x, y, w, h))
        open_cv_image = np.array(im1)

        # Convert OpenCV Image to QImage to set as QPixMap
        height, width, channel = open_cv_image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(open_cv_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.sudoku_image.setPixmap(QtGui.QPixmap(qImg))

        # Set the opacity level to be slightly transparent
        op = QtWidgets.QGraphicsOpacityEffect(self.sudoku_image)
        op.setOpacity(0.3)
        self.sudoku_image.setGraphicsEffect(op)

        # Set the stack to display the image
        self.stack_layer = 1
        self.main_stack.setCurrentIndex(self.stack_layer)

        # Make sure that the loading text QLabel is centered and visible
        center = self.capture_widget.geometry().center()
        self.loading_label.setGeometry(center.x() - 80, center.y(), 230, 40)
        self.loading_label.setVisible(True)

        # Disable the mask to display the captured sudoku image
        self.screen_capture_enabled = False
        self.updateMask()
        QApplication.processEvents()

        return open_cv_image

    def get_sudoku_board_from_screen(self):
        self.status_text.setText('Reading sudoku board from screen...')
        QApplication.processEvents()

        grabGeometry = self.capture_widget.geometry()
        grabGeometry.moveTopLeft(self.capture_widget.mapToGlobal(QtCore.QPoint(0, 0)))
        x = grabGeometry.left()
        y = grabGeometry.top()
        w = grabGeometry.width()
        h = grabGeometry.height()

        self.image_corner_x = x
        self.image_corner_y = y

        open_cv_image = self.display_loading_screen(x, y, w, h)
        self.reader.get_sudoku_board(x, y, w, h, open_cv_image)

    def solve_loaded_sudoku_board(self):
        self.loading_label.setVisible(False)
        self.status_text.setText('Solving sudoku puzzle!')
        QApplication.processEvents()

        print(self.reader.game_board)

        self.solver.load_board(self.reader.game_board)
        has_solution = self.solver.solve_sudoku()
        self.capture_widget.valid_board(has_solution)
        self.fill_button.setEnabled(has_solution)
        self.grid_values = self.solver.solution
        return has_solution

    def button_solve_clicked(self):
        self.get_sudoku_board_from_screen()
        self.solve_button.setEnabled(False)
        has_solution = self.solve_loaded_sudoku_board()
        self.populate_grid()
        self.stack_layer = 0
        self.sudoku_image.clear()
        self.main_stack.setCurrentIndex(self.stack_layer)

        if has_solution:
            self.status_text.setText('Solution to sudoku puzzle')
        else:
            self.status_text.setText('Invalid sudoku board; no solution available')
        QApplication.processEvents()

    def button_clear_clicked(self):
        self.stack_layer = 1
        self.main_stack.setCurrentIndex(self.stack_layer)
        self.grid_values = None
        self.image_corner_x = None
        self.image_corner_y = None
        self.screen_capture_enabled = True
        self.solve_button.setEnabled(True)
        self.fill_button.setEnabled(False)
        self.updateMask()
        self.status_text.setText('Please position window over sudoku on screen!')

    def button_fill_clicked(self):
        if self.image_corner_x is None or self.image_corner_y is None:
            return
        self.screen_capture_enabled = True
        self.updateMask()
        self.writer.load_solution_board(self.image_corner_x, self.image_corner_y,
                                        self.solver.solution, self.reader.game_board_contours)
        self.writer.find_game_board_centers()
        self.writer.write_in_sudoku()
        self.setFocus(True)
        self.button_clear_clicked()

    def populate_grid(self):
        if self.grid_values is not None:
            self.capture_widget.populate_board(self.grid_values)
