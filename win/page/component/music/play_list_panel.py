from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QGridLayout, QHBoxLayout, QPushButton, QStyle, \
    QStyleFactory, QSplitter
from qtawesome import icon

from win.generator.scaled_image import get_fixed_image
from win.page.component.music.play_list import MusicPlayList

style = """
#tabsublabel{
    color: grey;
}
"""


class PlayListPanel(QWidget):

    def __init__(self, listname, description, parent=None):
        super(PlayListPanel, self).__init__(parent)

        # 最上方
        self.title = QLabel(listname, font=QFont('黑体', 20, weight=QFont.Bold))
        self.subTitle = QLabel(description, font=QFont('黑体', 12))
        self.subTitle.setObjectName('tabsublabel')
        self.subTitle.setStyleSheet(style)
        self.createTimeLabel = QLabel('2020-11-27创建', font=QFont('黑体', 10))
        self.createTimeLabel.setObjectName('tabsublabel')
        self.createTimeLabel.setStyleSheet(style)
        self.playall_btn = QPushButton('播放全部', icon=icon('mdi.play-circle-outline', color='#fff'))
        self.playall_btn.setStyle(QStyleFactory.create('fusion'))
        self.playall_btn.setStyleSheet("background-color:#418AE4;color:#fff;")
        self.downloadall_btn = QPushButton('下载全部', icon=icon('mdi.download'))
        self.downloadall_btn.setStyle(QStyleFactory.create('fusion'))
        self.output_btn = QPushButton('导出歌单', icon=icon('mdi.file-download-outline'))
        self.output_btn.setStyle(QStyleFactory.create('fusion'))
        self.btnlayout = QHBoxLayout()
        self.btnlayout.addWidget(self.playall_btn)
        self.btnlayout.setSpacing(10)
        self.btnlayout.addWidget(self.downloadall_btn)
        self.btnlayout.setSpacing(10)
        self.btnlayout.addWidget(self.output_btn)
        self.titleLayout = QVBoxLayout()
        self.titleLayout.setAlignment(Qt.AlignTop)
        self.titleLayout.setSpacing(10)
        self.titleLayout.addWidget(self.title)
        self.titleLayout.setSpacing(10)
        self.titleLayout.addWidget(self.createTimeLabel)
        self.titleLayout.setSpacing(10)
        self.titleLayout.addLayout(self.btnlayout)
        self.titleLayout.setSpacing(10)
        self.titleLayout.addWidget(self.subTitle)
        self.songnum_label = QLabel('歌曲数', font=QFont('黑体', 10))
        self.songnum_label.setStyleSheet('color:grey;')
        self.song_num = QLabel('100', font=QFont('黑体', 10, weight=QFont.Bold))
        self.song_num.setStyleSheet('color:grey;')
        self.playnum_label = QLabel('播放数', font=QFont('黑体', 10))
        self.playnum_label.setStyleSheet('color:grey;')
        self.play_num = QLabel('1220', font=QFont('黑体', 10, weight=QFont.Bold))
        self.play_num.setStyleSheet('color:grey;')
        self.group1 = QVBoxLayout()
        self.group1.setAlignment(Qt.AlignVCenter)
        self.group1.addWidget(self.songnum_label)
        self.group1.setSpacing(5)
        self.group1.addWidget(self.song_num)
        self.group2 = QVBoxLayout()
        self.group2.setAlignment(Qt.AlignVCenter)
        self.group2.addWidget(self.playnum_label)
        self.group2.setSpacing(5)
        self.group2.addWidget(self.play_num)
        self.numGroupLayout = QHBoxLayout()
        self.numGroupLayout.setAlignment(Qt.AlignHCenter)
        self.numGroupLayout.addLayout(self.group1)
        self.numGroupLayout.addWidget(QSplitter())
        self.numGroupLayout.addLayout(self.group2)

        self.hbox = QHBoxLayout()
        self.hbox.setAlignment(Qt.AlignLeft)
        self.hbox.addWidget(get_fixed_image('res/album.jpg'))
        self.hbox.setSpacing(20)
        self.hbox.addLayout(self.titleLayout)
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.numGroupLayout)

        self.music_play_list = MusicPlayList()

        # 歌曲的id
        self.song_ids = []

        self.vbox = QVBoxLayout(self)
        self.vbox.addLayout(self.hbox)
        # self.vbox.setSpacing(50)
        self.vbox.addWidget(self.get_music_list_title())
        self.vbox.addWidget(self.music_play_list)


    def get_music_list_title(self):
        wight = QWidget()
        self.layout_main = QGridLayout()
        album_label = QLabel()
        album_label.setText('专辑')
        album_label.setStyleSheet('color: #418AE4;')
        album_label.setObjectName('music_album_label')

        artist_label = QLabel()
        artist_label.setText('歌手')
        artist_label.setStyleSheet('color: #418AE4;')
        artist_label.setObjectName('music_artist_label')

        name_label = QLabel()
        name_label.setText('歌曲名')
        name_label.setStyleSheet('color: #418AE4;')
        name_label.setObjectName('music_name_label')

        self.layout_main.addWidget(name_label, 1, 1, 1, 5)
        self.layout_main.addWidget(artist_label, 1, 6, 1, 5)
        self.layout_main.addWidget(album_label, 1, 10, 1, 5)
        wight.setLayout(self.layout_main)
        return wight


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = PlayListPanel('当前播放', '哈哈哈哈啊哈哈')
    gui.show()
    sys.exit(app.exec_())
