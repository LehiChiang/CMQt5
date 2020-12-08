from PyQt5.QtCore import pyqtSignal, QThread


class CMThread(QThread):

    signal = pyqtSignal(str)

    def __init__(self):
        super(CMThread, self).__init__()

    def run(self):
        # do something
        self.signal.emit(' ')
