import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget

from mainwindow import SudokuSolver


# Set the colour palette of the UI
# Defaults to a dark mode configuration
#   @param mode: The mode to which the palette of the GUI should be set to
#   @return palette: The palette with which to apply on the GUI
def set_colour_palette(mode="dark mode"):

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))           # Window colour
    palette.setColor(QPalette.WindowText, Qt.white)                 # Window text colour
    palette.setColor(QPalette.Base, QColor(25, 25, 25))             # Background colour 1
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))    # Background colour 2
    palette.setColor(QPalette.ToolTipBase, Qt.white)                # Tool tip background colour
    palette.setColor(QPalette.ToolTipText, Qt.white)                # Tool tip text colour
    palette.setColor(QPalette.Text, Qt.white)                       # Text colour
    palette.setColor(QPalette.Button, QColor(53, 53, 53))           # Button colour
    palette.setColor(QPalette.ButtonText, Qt.white)                 # Button text colour
    palette.setColor(QPalette.BrightText, Qt.red)                   # Highlight text colour
    palette.setColor(QPalette.Link, QColor(42, 130, 218))           # Link colour
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))      # Highlight colour
    palette.setColor(QPalette.HighlightedText, Qt.black)            # Highlighted text colour

    return palette


# Main function that runs the QApplication
def main():

    # Creates the application GUI object
    app = QApplication(sys.argv)

    # Sets the style and the palette
    app.setStyle("Fusion")                      # Fusion for the same style across all platforms
    app.setPalette(set_colour_palette())        # Palette set to dark mode

    # Run the main window object
    ex = SudokuSolver()
    ex.show()

    # Exit when the application is quit by the user
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
