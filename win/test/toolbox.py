from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QWidget, QPushButton


class MyWin(QWidget):

    def __init__(self):
        super(MyWin, self).__init__()
        self.setWindowTitle("QToolBox")
        self.resize(500, 700)

        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)

        for i in range(10):
            if not hasattr(self, 'btn_{}'.format(i)):
                btn = QPushButton('btn_{}'.format(i))
                setattr(self, 'btn_{}'.format(i), btn)
                getattr(self, 'btn_{}'.format(i)).clicked.connect(lambda: self.printHello(self.sender().text()))
                self.vbox.addWidget(getattr(self, 'btn_{}'.format(i)))

    def printHello(self, i):
        print(i)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
