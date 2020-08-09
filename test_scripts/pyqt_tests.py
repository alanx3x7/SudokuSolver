import sys
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QWidget


class ZoomWidget(QWidget):

    def __init__(self, parent=None):
        super(ZoomWidget, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_NoSystemBackground)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color:transparent;")
        self.setGeometry(100, 100, 100, 100)
        frameRect = self.frameGeometry()
        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        region = QtGui.QRegion(frameRect.adjusted(-10, -10, 10, 10))
        print(frameRect)
        print(self.isWindow())
        self.setMask(region)
        self.show()

    def paintEvent(self, e=None):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.gray, 3, QtCore.Qt.DashDotLine))
        qp.drawRect(0, 0, self.rect().width()-1, self.rect().height()-1)
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ZoomWidget()
    sys.exit(app.exec_())
