from sys import argv

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStyleFactory, \
    QListWidget, QApplication, QListWidgetItem, QGridLayout, QAbstractItemView


class PlayListDrawerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(PlayListDrawerWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(300)
        self.setObjectName('PlayListDrawerWidget')
        self.setStyleSheet('PlayListDrawerWidget{background:white;}')
        self.musicNum = 0
        # 歌曲的id
        self.song_ids = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)

        top_layout = QHBoxLayout(self)
        top_layout.setContentsMargins(10, 0, 10, 0)
        self.top_label = QLabel(self)
        self.top_label.setText('播放队列(共{}首)'.format(self.musicNum))
        self.top_clear_btn = QPushButton(self)
        self.top_clear_btn.setText('清空')
        self.top_clear_btn.setStyle(QStyleFactory.create('fusion'))
        top_layout.addWidget(self.top_label, alignment=Qt.AlignLeft)
        top_layout.addWidget(self.top_clear_btn, alignment=Qt.AlignRight)

        self.music_play_list = PlayListDrawerList()
        # mlist = [{'id': 1, 'artist': 'aaaa', 'name': '1111'}, {'id': 2, 'artist': 'bbbb', 'name': '2222'},
        #          {'id': 3, 'artist': 'cccc', 'name': '33333'}]
        # for item in mlist:
        #     self.add_music_tile(item)
        layout.addLayout(top_layout)
        layout.addWidget(self.music_play_list)


class PlayListDrawerList(QListWidget):
    def __init__(self, *args, **kwargs):
        super(PlayListDrawerList, self).__init__(*args, **kwargs)
        self.css = """
            QListWidget#drawer_music_list{
                 outline: 0px;
                 alternate-background-color: rgb(255, 255, 255);
                 border: none;
            }
            QListWidget#drawer_music_list::Item{
                 height:60px;
                 border: none;
                 background: none;
            }
            QListWidget#drawer_music_list::Item:hover{
                background: rgb(240, 241, 241);
            }
            QListWidget#drawer_music_list::Item:selected {
                background: rgb(240, 241, 241);
                color: #fff;
            }
            QListView#drawer_music_list::item:!alternate:!selected{
                background: rgb(249, 249, 249);
            }
        """
        self.setObjectName('drawer_music_list')
        self.setStyleSheet(self.css)
        self.setFont(QFont('黑体', 11))
        self.setViewMode(QListWidget.ListMode)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContextMenuPolicy(3)
        self.setAlternatingRowColors(True)

    def add_music_tile(self, music: dict):
        item = QListWidgetItem()
        item.setWhatsThis(str(music['id']))
        self.insertItem(0, item)
        self.setItemWidget(item, PlayListDrawerListItem(music['artist'], music['name'], music['duration']))


class PlayListDrawerListItem(QWidget):
    def __init__(self, artist, name, duration, *args, **kwargs):
        super(PlayListDrawerListItem, self).__init__(*args, **kwargs)
        self.css = """
                QLabel#drawer_music_artist_label{
                    color:rgb(135,135,135) !important;
                }
                QLabel#drawer_music_name_label{
                    color:rgb(83,83,83) !important;
                }
                """
        self.setStyleSheet(self.css)
        layout_main = QGridLayout()
        artist_label = QLabel()
        artist_label.setFont(QFont('宋体', 12))
        artist_label.setObjectName('drawer_music_artist_label')
        artist_label.setText(QFontMetrics(artist_label.font()).elidedText(artist, Qt.ElideRight, 210))
        artist_label.setToolTip(artist)
        name_label = QLabel()
        name_label.setFont(QFont('宋体', 14))
        name_label.setObjectName('drawer_music_name_label')
        name_label.setText(QFontMetrics(name_label.font()).elidedText(name, Qt.ElideRight, 210))
        name_label.setToolTip(name)

        duration_label = QLabel()
        duration_label.setFont(QFont('宋体', 12))
        duration_label.setObjectName('drawer_music_duration_label')
        duration_label.setText(duration)
        duration_label.setToolTip(duration)
        layout_main.addWidget(name_label, 1, 1, 1, 5)
        layout_main.addWidget(artist_label, 2, 1, 1, 5)
        layout_main.addWidget(duration_label, 1, 5, 2, 1)
        self.setLayout(layout_main)


if __name__ == '__main__':
    app = QApplication(argv)
    drawer = PlayListDrawerWidget()
    drawer.show()
    exit(app.exec_())
