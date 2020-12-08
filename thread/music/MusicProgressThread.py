from PyQt5.QtCore import pyqtSignal, QThread


class MusicProgressThread(QThread):

    progressbarSignal = pyqtSignal(int)

    def __init__(self, position, curPos, current_time, total_time, duration):
        super(MusicProgressThread, self).__init__()
        self.position = position
        self.__curPos = curPos
        self.current_time = current_time
        self.total_time = total_time
        self.__duration = duration

    def run(self):
        try:
            secs = self.position / 1000
            mins = secs / 60
            secs = secs % 60
            self.__curPos = "%2d:%2d" % (mins, secs)
            self.current_time.setText(self.__curPos)
            self.total_time.setText(self.__duration)
            self.progressbarSignal.emit(self.position)
        except Exception as e:
            print(e)
