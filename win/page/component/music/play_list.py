from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem, QWidget, QGridLayout, QLabel, QToolButton, \
    QMenu, QAction
from qtawesome import icon


class MusicPlayList(QListWidget):

    def __init__(self):
        super(MusicPlayList, self).__init__()
        self.css = """
            QListWidget#music_list{
                 outline: 0px;
                 background-color:transparent;
                 border: none;
            }
            QListWidget#music_list::Item{
                 height:42px;
                 border: none;
                 background: none;
            }
            QListWidget#music_list::Item:hover{
                background: skyblue;
            }
            QListWidget#music_list::Item:selected {
                background: skyblue;
                color: #fff;
            }
        """
        self.setObjectName('music_list')
        self.setStyleSheet(self.css)
        self.setFont(QFont('黑体', 11))
        # self.setMinimumHeight(240)
        self.setViewMode(QListWidget.ListMode)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContextMenuPolicy(3)
        # self.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)

    def add_Music_Tile(self, music: dict):
        item = QListWidgetItem()
        item.setWhatsThis(str(music['id']))
        self.insertItem(0, item)
        self.setItemWidget(item, self.get_Item_Widget(music['album'], music['artist'], music['name']))

    def get_Item_Widget(self, album, artist, name):
        wight = QWidget()
        self.layout_main = QGridLayout()
        album_label = QLabel()
        album_label.setText(album)
        album_label.setWordWrap(True)
        album_label.setObjectName('music_album_label')

        artist_label = QLabel()
        artist_label.setText(artist)
        artist_label.setWordWrap(True)
        artist_label.setObjectName('music_artist_label')

        name_label = QLabel()
        name_label.setText(name)
        name_label.setWordWrap(True)
        name_label.setObjectName('music_name_label')

        self.layout_main.addWidget(name_label, 1, 1, 1, 5)
        self.layout_main.addWidget(artist_label, 1, 6, 1, 5)
        self.layout_main.addWidget(album_label, 1, 10, 1, 5)
        wight.setLayout(self.layout_main)
        return wight

    # def myListWidgetContext(self, point: QPoint):
    #     item = self.itemAt(point.x(), point.y())
    #     if item!=None:
    #         popMenu = QMenu()
    #         deleteAction = QAction(u'删除', self)
    #         deleteAction.setIcon(icon('mdi.trash-can-outline'))
    #         deleteAction.triggered.connect(self.delete_action)
    #
    #         popMenu.addAction(deleteAction)
    #         popMenu.addAction(QAction(u'修改', self))
    #         popMenu.exec_(QCursor.pos())
    #
    # def delete_action(self):
    #     print(self.currentRow())
    #     item = self.currentItem()
    #     self.takeItem(self.row(item))
