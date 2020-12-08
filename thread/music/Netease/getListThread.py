from PyQt5.QtCore import pyqtSignal, QThread

from service.music.NeteaseMusic import NeteaseMusic


class getList(QThread):

    signal = pyqtSignal(list)

    def __init__(self, music_name):
        super(getList, self).__init__()
        self.music_name = music_name

    def run(self):
        try:
            music = NeteaseMusic()
            music_list = music.get_music_list(self.music_name, 20, 1, 1)
            self.signal.emit(music_list)
        except Exception as e:
            print(e)
