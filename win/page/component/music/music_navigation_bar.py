import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, QSlider, QStyleFactory, QLabel, QToolButton, QVBoxLayout
from qtawesome import icon

from win.CM.CMCircleButton import CMCircleButton


class MusicPlayer(QWidget):
    """
    音乐播放的导航栏
    """

    def __init__(self):
        super(MusicPlayer, self).__init__()
        self.init_ui()

        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.__duration = ''
        self.__curPos = ''
        self.currentMusicId = ''

        self.player.positionChanged.connect(self.do_positionChanged)
        self.player.durationChanged.connect(self.do_durationChanged)

    def init_ui(self):

        self.setFixedHeight(60)
        self.navbar_main_layout = QHBoxLayout(self)
        self.setObjectName('nav_bar')
        self.setStyleSheet(self.css())
        self.navbar_main_layout.setAlignment(Qt.AlignVCenter)
        self.navbar_main_layout.setContentsMargins(0, 0, 0, 0)

        self.play_button = CMCircleButton(radius=20)
        self.play_button.setIcon(icon('mdi.play', color='#fff'))
        self.play_button.setToolTip('播放')
        self.previous_button = CMCircleButton(radius=20)
        self.previous_button.setIcon(icon('mdi.skip-previous', color='#fff'))
        self.previous_button.setToolTip('上一首歌曲')
        self.next_button = CMCircleButton(radius=20)
        self.next_button.setIcon(icon('mdi.skip-next', color='#fff'))
        self.next_button.setToolTip('下一首歌曲')
        self.total_time = QLabel('00:00')
        self.total_time.setObjectName('music_time')
        self.total_time.setStyle(QStyleFactory.create('Fusion'))

        # self.play_slider = QSlider(Qt.Horizontal, self)
        # self.play_slider.valueChanged[int].connect(lambda: self.player.setPosition(self.play_slider.value()))
        # self.play_slider.setStyle(QStyleFactory.create('Fusion'))
        # self.play_slider.setCursor(QCursor(Qt.PointingHandCursor))
        # self.play_slider.setSingleStep(0)
        # self.play_slider.setToolTip('拖动滑块快进/快退')

        self.vol_slider = QSlider(Qt.Horizontal, self)
        self.vol_slider.setStyle(QStyleFactory.create('Fusion'))
        self.vol_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.vol_slider.setMaximumWidth(120)
        self.vol_slider.setValue(20)
        self.current_vol = self.vol_slider.value()  # 默认音量
        self.vol_slider.valueChanged[int].connect(self.setMusicVolumn)

        self.mute_btn = QToolButton()
        self.mute_btn.setCheckable(True)
        self.mute_btn.setIcon(icon('mdi.volume-high', color='#418AE4'))
        self.mute_btn.setIconSize(QSize(28, 28))
        self.mute_btn.setObjectName('mute_btn')
        self.mute_btn.setStyleSheet('#mute_btn{border: none; background-color: none;}')
        self.mute_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mute_btn.clicked.connect(self.mute_switch)
        self.mute_btn.setToolTip('静音')

        self.playlist_btn = QToolButton()
        self.playlist_btn.setCheckable(True)
        self.playlist_btn.setIcon(icon('mdi.playlist-music-outline', color='#6F6F6F'))
        self.playlist_btn.setIconSize(QSize(32, 32))
        self.playlist_btn.setObjectName('playlist_btn')
        self.playlist_btn.setStyleSheet('#playlist_btn{border: none; background-color: none;}')
        self.playlist_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.playlist_btn.clicked.connect(self.playlist_switch)
        self.playlist_btn.setToolTip('打开播放列表')

        self.navbar_main_layout.addWidget(self.previous_button)
        self.navbar_main_layout.addWidget(self.play_button)
        self.navbar_main_layout.addWidget(self.next_button)
        self.navbar_main_layout.addStretch(5)
        self.navbar_main_layout.addWidget(self.build_music_window())
        self.navbar_main_layout.addStretch(5)
        self.navbar_main_layout.addWidget(self.total_time)
        self.navbar_main_layout.addWidget(self.mute_btn)
        self.navbar_main_layout.addWidget(self.vol_slider)
        self.navbar_main_layout.addWidget(self.playlist_btn)

    def build_music_window(self):
        self.music_window = QWidget()
        self.music_window.setFixedWidth(200)
        self.music_window_layout = QHBoxLayout()
        self.music_window_layout.setContentsMargins(0, 0, 0, 0)

        self.music_pic = QLabel()
        self.music_window_layout.addWidget(self.music_pic)
        self.music_info_layout = QVBoxLayout()
        self.music_info_layout.setAlignment(Qt.AlignLeft)
        self.music_window_title = QLabel()
        self.music_window_author = QLabel()
        self.music_info_layout.addWidget(self.music_window_title)
        self.music_info_layout.addWidget(self.music_window_author)
        self.music_window_layout.addLayout(self.music_info_layout)

        self.music_window.setLayout(self.music_window_layout)
        return self.music_window

    def mute_switch(self):
        if self.mute_btn.isChecked():
            self.vol_slider.setValue(0)
            self.player.setVolume(0)
            self.mute_btn.setIcon(icon('mdi.volume-mute', color='#6F6F6F'))
            self.mute_btn.setToolTip('打开声音')
        else:
            self.vol_slider.setValue(self.current_vol)
            self.mute_btn.setIcon(icon('mdi.volume-high', color='#418AE4'))
            self.mute_btn.setToolTip('静音')

    def setMusicVolumn(self, volumn):
        if volumn == 0:
            self.mute_btn.setChecked(True)
            self.mute_btn.setIcon(icon('mdi.volume-mute', color='#6F6F6F'))
            self.mute_btn.setToolTip('打开声音')
        else:
            self.current_vol = volumn
            self.player.setVolume(volumn)
            self.mute_btn.setChecked(False)
            self.mute_btn.setIcon(icon('mdi.volume-high', color='#418AE4'))
            self.mute_btn.setToolTip('静音')

    def playlist_switch(self):

        if self.playlist_btn.isChecked():
            self.playlist_btn.setIcon(icon('mdi.playlist-music', color='#418AE4'))
            self.playlist_btn.setToolTip('关闭播放列表')
        else:
            self.playlist_btn.setIcon(icon('mdi.playlist-music-outline', color='#6F6F6F'))
            self.playlist_btn.setToolTip('打开播放列表')

    def do_positionChanged(self, position):
        secs = position/1000
        mins = secs / 60
        secs = secs % 60
        self.__curPos = "%2d:%2d"%(mins, secs)
        self.total_time.setText(self.__curPos+'/'+self.__duration)


    def do_durationChanged(self, duration):
        secs = duration / 1000
        mins = secs / 60
        secs = secs % 60
        self.__duration = "%d:%d" % (mins, secs)
        self.total_time.setText(self.__curPos+'/'+self.__duration)

    def css(self):
        return """
            QWidget#nav_bar{
                border-top: 10px solid lightgrey;
                background: #ECF1FA !important;
                padding: 0px;
            }
            QToolButton#mute_btn{
                border: none;
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MusicPlayer()
    gui.show()
    sys.exit(app.exec_())
