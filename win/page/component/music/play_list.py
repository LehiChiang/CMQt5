from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem, QWidget, QGridLayout, QLabel


class MusicPlayList(QListWidget):

    def __init__(self):
        super(MusicPlayList, self).__init__()
        self.css = """
            QListWidget#music_list{
                 outline: 0px;
                 alternate-background-color: rgb(255, 255, 255);
                 border: none;
            }
            QListWidget#music_list::Item{
                 height:42px;
                 border: none;
                 background: none;
            }
            QListWidget#music_list::Item:hover{
                background: rgb(240, 241, 241);
            }
            QListWidget#music_list::Item:selected {
                background: rgb(240, 241, 241);
                color: #fff;
            }
            QListView#music_list::item:!alternate:!selected{
                background: rgb(249, 249, 249);
            }
        """
        self.setObjectName('music_list')
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
        self.setItemWidget(item, MusicPlayListItem(music['album'], music['artist'], music['name']))


class MusicPlayListItem(QWidget):

    def __init__(self, album, artist, name):
        super(MusicPlayListItem, self).__init__()
        layout_main = QGridLayout()
        album_label = QLabel()
        album_label.setObjectName('music_album_label')
        album_label.setText(QFontMetrics(album_label.font()).elidedText(album, Qt.ElideRight, 160))
        album_label.setToolTip(album)

        artist_label = QLabel()
        artist_label.setObjectName('music_artist_label')
        artist_label.setText(QFontMetrics(artist_label.font()).elidedText(artist, Qt.ElideRight, 160))
        artist_label.setToolTip(artist)

        name_label = QLabel()
        name_label.setObjectName('music_name_label')
        name_label.setText(QFontMetrics(name_label.font()).elidedText(name, Qt.ElideRight, 160))
        name_label.setToolTip(name)

        layout_main.addWidget(name_label, 1, 1, 1, 5)
        layout_main.addWidget(artist_label, 1, 6, 1, 5)
        layout_main.addWidget(album_label, 1, 10, 1, 5)
        self.setLayout(layout_main)
