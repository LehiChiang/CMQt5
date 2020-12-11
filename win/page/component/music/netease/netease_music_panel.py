from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication, QListWidget, \
    QListWidgetItem, QGridLayout, QAbstractItemView

from thread.music.Netease.getListThread import getList
from win.CM.CMInputBox import CMInputBox

style = """
#tablabel{
    padding: 5px 0px 5px 0px;
}
#tabsublabel{
    padding: 10px 0px;
    color: grey;
}
"""


def get_music_list_title():
    wight = QWidget()
    layout_main = QGridLayout()
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

    layout_main.addWidget(name_label, 1, 1, 1, 5)
    layout_main.addWidget(artist_label, 1, 6, 1, 5)
    layout_main.addWidget(album_label, 1, 10, 1, 5)
    wight.setLayout(layout_main)
    return wight


def get_item_widget(album, artist, name):
    layout_main = QGridLayout()
    wight = QWidget()
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
    wight.setLayout(layout_main)
    return wight


class NeteaseMusicSearchedPanel(QWidget):

    def __init__(self, parent=None):
        super(NeteaseMusicSearchedPanel, self).__init__(parent)

        # 最上方
        self.title = QLabel('搜索音乐', font=QFont('黑体', 20))
        self.title.setObjectName('tablabel')
        self.title.setStyleSheet(style)
        self.subTitle = QLabel('提供网易云的音乐搜索接口', font=QFont('黑体', 12))
        self.subTitle.setObjectName('tabsublabel')
        self.subTitle.setStyleSheet(style)

        self.search_box = CMInputBox(color='#418AE4')
        self.search_box.leading.triggered.connect(self.search_action)
        self.search_box.returnPressed.connect(self.search_action)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.search_box)
        self.hbox.addStretch(1)

        self.music_result_list = MusicResultList()

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.subTitle)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(get_music_list_title())
        self.vbox.addWidget(self.music_result_list)

    def search_action(self):
        self.music_thread = getList(music_name=self.search_box.text())
        self.music_thread.signal.connect(self.search_results_callback)
        self.music_thread.start()

    def search_results_callback(self, music_list):
        try:
            self.music_result_list.set_music_list(music_list)
        except Exception as e:
            print(e)


class MusicResultList(QListWidget):
    def __init__(self):
        super(MusicResultList, self).__init__()
        self.music_list = None
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
        self.setViewMode(QListWidget.ListMode)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setContextMenuPolicy(3)

    def set_music_list(self, music_list):
        self.music_list = music_list
        self.construct_music_list()

    def construct_music_list(self):
        self.clear()
        for music in self.music_list:
            item = QListWidgetItem()
            item.setWhatsThis(str(music['id']))
            self.addItem(item)
            self.setItemWidget(item, get_item_widget(music['album'], music['artist'], music['name']))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = NeteaseMusicSearchedPanel()
    gui.show()
    sys.exit(app.exec_())
