# Normal system imports
import sys
import numpy as np
import pyautogui

# PyQt5 imports
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# Class object imports
from BoardWindow import BoardWindow
from SudokuScreenReader import SudokuScreenReader
from SudokuScreenWriter import SudokuScreenWriter
from SudokuRecursiveSolver import SudokuRecursiveSolver


class SudokuSolver(QWidget):
    """ SudokuSolver QWidget that is the main window of the application """

    # To keep track of whether the mask has been initialized or not
    dirty = True

    def __init__(self, parent=None):
        """ Constructor
            :param parent: Parent of this widget
        """
        super(SudokuSolver, self).__init__(parent)

        # Creates the SudokuScreenReader, SudokuScreenWriter, and SudokuRecursiveSolver objects
        self.reader = SudokuScreenReader()
        self.writer = SudokuScreenWriter()
        self.solver = SudokuRecursiveSolver()

        # Initializes member variables so PyCharm does not complain
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

        # Set the window characteristics
        self.setWindowTitle('Sudoku Solver')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowIcon(QtGui.QIcon('../data/sudoku_solver_icon.png'))

        # Which layer of the stacked widget is to be displayed
        self.stack_layer = 0

        # To hold the window corner coordinates so the SudokuScreenWriter knows where to write its output
        self.image_corner_x = None
        self.image_corner_y = None

        # Controls whether masking should be enabled to allow the window to be see through for sudoku puzzle capture
        self.screen_capture_enabled = True

        # Organize the UI, and set the layout of the main window to be the main layout
        self.initUI()
        self.setLayout(self.main_layout)

        self.show()

    def initUI(self):
        """ Initialize the GUI by placing the objects in the correct positions
            :return: None
        """

        # Create the main layout and sets the margins
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setContentsMargins(10, 5, 10, 5)

        # Create the status text label widget and place it on top of the GUI
        self.status_text = QtWidgets.QLabel()
        self.status_text.setText('Please position window over sudoku on screen!')
        self.status_text.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.main_layout.addWidget(self.status_text)

        # Create a stacked widget that holds the screenshot of the puzzle and the solution to the puzzle
        self.main_stack = QtWidgets.QStackedWidget(self)

        # Create sudoku board widget that will hold the solution to the solved sudoku puzzle
        self.capture_widget = BoardWindow()
        self.capture_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Create a label widget that will hold the screenshot of the captured sudoku puzzle
        self.sudoku_image = QtWidgets.QLabel(self)

        # Add the sudoku board widget and sudoku screenshot widget to the stack widget, and set default to board widget
        self.main_stack.addWidget(self.capture_widget)
        self.main_stack.addWidget(self.sudoku_image)
        self.main_stack.setCurrentIndex(self.stack_layer)
        self.main_layout.addWidget(self.main_stack)

        # Create the button layout to hold the buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        # Create a clear button that clears the solution board and enables capture of a new sudoku puzzle
        self.clear_button = QtWidgets.QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.button_clear_clicked)
        self.clear_button.setEnabled(True)
        self.button_layout.addWidget(self.clear_button)

        # Create a solve button that causes the sudoku puzzle in the window to be captured and solved
        self.solve_button = QtWidgets.QPushButton('Solve', self)
        self.solve_button.clicked.connect(self.button_solve_clicked)
        self.solve_button.setEnabled(True)
        self.button_layout.addWidget(self.solve_button)

        # Create a fill button that automatically fills the sudoku puzzle on screen with the solution computed
        self.fill_button = QtWidgets.QPushButton('Fill', self)
        self.fill_button.clicked.connect(self.button_fill_clicked)
        self.fill_button.setEnabled(False)
        self.button_layout.addWidget(self.fill_button)

        # Label to be placed over the screenshot of the sudoku puzzle to inform the user of operation stages
        self.loading_label = QtWidgets.QLabel(self)
        self.loading_label.setText('Reading numbers from image...')
        self.loading_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.main_layout.addLayout(self.button_layout)

    def updateMask(self):
        """ Update the mask on the GUI to allow a see-through window in the GUI for screen capture for
            the SudokuScreenReader
            :return: None
        """
        # Get the GUI frame and capture widget geometries
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

        # Subtract the region containing the capture window if screen capture mode is enabled
        if self.screen_capture_enabled:
            region -= QtGui.QRegion(captureRect)

        # Set the mask
        self.setMask(region)

    def paintEvent(self, event):
        """ On every update call if something in the GUI is changed
            :param event: Event handler that calls this function [event]
            :return: None
        """
        super(SudokuSolver, self).paintEvent(event)

        # Since there is nothing to update the paintEvent of this widget, only do this once
        if self.dirty:
            self.updateMask()
            self.dirty = False

    def resizeEvent(self, event):
        """ Called whenever the window is resized
            :param event: Event handler that calls this function [event]
            :return: None
        """
        super(SudokuSolver, self).resizeEvent(event)

        # Move the loading label to the center of the capture widget whenever the screen is resized
        center = self.capture_widget.geometry().center()
        self.loading_label.setGeometry(center.x() - 80, center.y(), 230, 40)

        # Updates the mask based on the new capture widget and window size
        if not self.dirty:
            self.updateMask()

    def display_loading_screen(self, x, y, w, h):
        """ Displays a screenshot of the sudoku puzzle and a loading message when SudokuScreenReader is
            reading the digits. This is done because the SudokuScreenReader may take a few seconds, and this
            provides visual feedback to the user.
        :param x: The x coordinate of the top left corner of the capture widget [int]
        :param y: The y coordinate of the top left corner of the capture widget [int]
        :param w: The width of the capture widget [int]
        :param h: The height of the capture widget [int]
        :return open_cv_image: Screenshot of puzzle to pass to SudokuScreenReader to read the digits
                               [CV::Mat or 3-channel 2D numpy array of int]
        """

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
        """ Use the SudokuScreenReader object to read the sudoku puzzle digits from screen
            :return: None
        """

        # Updates the status text for user feedback
        self.status_text.setText('Reading sudoku board from screen...')
        QApplication.processEvents()

        # Gets the geometry of the capture widget to know where to take a screenshot of the screen
        grabGeometry = self.capture_widget.geometry()
        grabGeometry.moveTopLeft(self.capture_widget.mapToGlobal(QtCore.QPoint(0, 0)))
        x = grabGeometry.left()
        y = grabGeometry.top()
        w = grabGeometry.width()
        h = grabGeometry.height()

        # Saves the corner location for the image for the SudokuScreenWriter later on
        self.image_corner_x = x
        self.image_corner_y = y

        # Update the GUI to display the loading screen, and reads the digits using SudokuScreenReader
        open_cv_image = self.display_loading_screen(x, y, w, h)
        self.reader.get_sudoku_board(x, y, w, h, open_cv_image)

    def solve_loaded_sudoku_board(self):
        """ Solves the sudoku puzzle that was read
            :return: None
        """

        # Hide the loading label and update the status text for user feedback
        self.loading_label.setVisible(False)
        self.status_text.setText('Solving sudoku puzzle!')
        QApplication.processEvents()

        # Prints the sudoku board that was read in for debugging
        print(self.reader.game_board)

        # Use the SudokuRecursiveSolver to solve the sudoku puzzle
        self.solver.load_board(self.reader.game_board)
        has_solution = self.solver.solve_sudoku()

        # Update the appearance of the board shown based on validity of the puzzle/solution
        self.capture_widget.valid_board(has_solution)   # Board is green if valid solution, red if invalid puzzle
        self.fill_button.setEnabled(has_solution)       # Fill button is enabled if valid solution, disabled if not
        self.grid_values = self.solver.solution
        return has_solution

    def button_solve_clicked(self):
        """ Called when the solve button is clicked
            :return: None
        """

        # Gets the sudoku board from the screen via screenshot
        self.get_sudoku_board_from_screen()
        self.solve_button.setEnabled(False)

        # Solves the sudoku board and updates the screen based on the solution
        has_solution = self.solve_loaded_sudoku_board()
        self.populate_grid()

        # Make the sudoku board on screen visible by changing the widget stack
        self.stack_layer = 0
        self.sudoku_image.clear()
        self.main_stack.setCurrentIndex(self.stack_layer)

        # Update status text based on whether the sudoku board has a valid solution or not
        if has_solution:
            self.status_text.setText('Solution to sudoku puzzle')
        else:
            self.status_text.setText('Invalid sudoku board; no solution available')
        QApplication.processEvents()

    def button_clear_clicked(self):
        """ Called when the clear button is clicked
            :return: None
        """

        # Sets the stack to display the sudoku image widget
        self.stack_layer = 1
        self.main_stack.setCurrentIndex(self.stack_layer)

        # Resets puzzle-dependent member variables
        self.grid_values = None
        self.image_corner_x = None
        self.image_corner_y = None

        # Enables and updates the mask, and disables the fill button
        self.screen_capture_enabled = True
        self.solve_button.setEnabled(True)
        self.fill_button.setEnabled(False)
        self.updateMask()
        self.status_text.setText('Please position window over sudoku on screen!')

    def button_fill_clicked(self):
        """ Called when the fill button is clicked
            :return: None
        """

        # If no image was taken then nothing happens
        if self.image_corner_x is None or self.image_corner_y is None:
            return

        # Enable screen capture and update mask to remove the sudoku solution from the screen
        # This enables us to click through the GUI and access the sudoku puzzle behind our GUI app
        self.screen_capture_enabled = True
        self.updateMask()

        # Use the SudokuScreenWriter to write the solution of the sudoku into the sudoku puzzle on screen
        self.writer.load_solution_board(self.image_corner_x, self.image_corner_y,
                                        self.solver.solution, self.reader.game_board_contours)
        self.writer.find_game_board_centers()
        self.writer.write_in_sudoku()
        self.setFocus(True)

        # Simulate a clear button click
        self.button_clear_clicked()

    def populate_grid(self):
        """ Populates the sudoku board widget with the values obtained from the SudokuRecursiveSolver
            :return: None
        """

        # Only update if we have values to update with though
        if self.grid_values is not None:
            self.capture_widget.populate_board(self.grid_values)
