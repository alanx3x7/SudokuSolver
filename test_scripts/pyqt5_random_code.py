# To import a gif
test_label = QtWidgets.QLabel(self)
test_label.setGeometry(180, 180, 50, 50)
gif = QtGui.QMovie("../data/loading.gif")
gif.setScaledSize(test_label.size())
test_label.setMovie(gif)
gif.start()