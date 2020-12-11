from PyQt5.QtCore import pyqtSignal, QThread

from service.music.NeteaseMusic import NeteaseMusic


class getSong(QThread):

    song_url = pyqtSignal(str, str, dict)

    def __init__(self, music_id):
        super(getSong, self).__init__()
        self.music_id = music_id

    def run(self):
        try:
            music = NeteaseMusic()
            code, music_url = music.get_music(self.music_id)
            print('Thread-getSong[music_id]:', self.music_id)
            _, music_info = music.get_music_info(self.music_id)
            # print('Thread-getSong[music_info]:', music_info)
            self.song_url.emit(self.music_id, music_url, music_info)
        except Exception as e:
            print(e)
