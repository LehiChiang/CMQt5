import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QApplication, QLabel

from win.CM.CMCollapsibleBox import CMCollapsibleBox
from win.CM.CMDialog import CMDialog
from win.CM.CMListButton import CMListButton
from win.CM.CMListLabel import CMListLabel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class MusicListPageLayout(QVBoxLayout):
    """
    音乐页面列表的内容layout，传入page
    """

    def __init__(self, MusicPageLayout):
        super(MusicListPageLayout, self).__init__()
        self.addWidget(MusicListPage(MusicPageLayout))
        self.setContentsMargins(0, 0, 0, 0)


class MusicListPage(QScrollArea):
    """
    音乐页面列表的内容
    """

    def __init__(self, MusicPageLayout):
        super(MusicListPage, self).__init__()
        self.MusicPageLayout = MusicPageLayout

        self.setObjectName('scroll')
        self.setStyleSheet(self.css())
        self.content = QWidget()
        self.content.setObjectName('scroll_content')
        self.content.setContentsMargins(0, 0, 0, 0)
        self.content.setStyleSheet("background:#F5F5F7 !important;")  ##F5F5F7

        self.setWidget(self.content)
        self.setWidgetResizable(True)

        self.item_layout = QVBoxLayout(self.content)
        self.item_layout.setContentsMargins(0, 0, 0, 0)
        self.item_layout.setSpacing(0)

        self.item_layout.addWidget(CMListLabel('搜索入口'))
        self.item_layout.addWidget(CMListButton('网易云音乐', 'fa.crosshairs',
                                                clicked=lambda: self.MusicPageLayout.music_stack.setCurrentIndex(1)))
        self.item_layout.addWidget(CMListButton('QQ音乐', 'fa.download', clicked=self.show_no_dialog))
        self.item_layout.addWidget(CMListButton('酷狗音乐', 'fa5.star', clicked=self.show_no_dialog))

        self.item_layout.addWidget(CMListButton('已播放', 'fa.list',
                                              clicked=lambda: self.MusicPageLayout.music_stack.setCurrentIndex(2)))

        self.list = os.listdir('config/playlist')
        song_list_item = QVBoxLayout()
        song_list_item.setContentsMargins(0, 0, 0, 0)
        song_list_box = CMCollapsibleBox("创建的歌单")
        for list in self.list:
            print("加载歌单：" + list)
            song_list_item.addWidget(CMListButton(list.split('.')[0], 'fa.list'))
        song_list_box.setContentLayout(song_list_item)
        self.item_layout.addWidget(song_list_box)
        self.item_layout.addStretch()

    def css(self):
        style = """#scroll{
                border:none;
            }"""
        return style

    def show_no_dialog(self):
        vbox = QVBoxLayout()
        label = QLabel('等待开发，谢谢！', font=QFont('黑体', 22))
        vbox.addLayout(centerlize(label))
        vbox.setSpacing(50)
        vbox.addWidget(get_scaled_image('res/svg/#418AE4/empty.png', 0.7))
        vbox.setAlignment(Qt.AlignHCenter)
        panel = QWidget()
        panel.setLayout(vbox)

        dia = CMDialog('错误', panel)
        dia.exec_()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MusicListPage()
    w.show()
    sys.exit(app.exec_())
