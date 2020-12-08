import requests
from PyQt5.QtCore import QUrl, QSize, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QCursor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QHBoxLayout, QWidget, QMessageBox, QMenu, QAction
from qtawesome import icon

from thread.music.Netease.getSongThread import getSong
from win.CM.CMRichPanel import CMRichPanel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image
from win.page.component.music.music_navigation_bar import MusicPlayer
from win.page.component.music.netease.netease_music_panel import NeteaseMusicSearchedPanel
from win.page.component.music.play_list_panel import PlayListPanel


class MusicPageLayout(QVBoxLayout):
    """
    页面内容的layout，传入page
    """
    def __init__(self):
        super(MusicPageLayout, self).__init__()
        self.music_stack = QStackedWidget()
        self.music_stack.setContentsMargins(10, 10, 10, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # 音乐播放导航栏
        self.music_player = MusicPlayer()
        self.music_player.setContentsMargins(0, 0, 0, 0)
        self.music_player.play_button.clicked.connect(self.play_music)
        self.music_player.previous_button.clicked.connect(self.previous_music)
        self.music_player.next_button.clicked.connect(self.next_music)
        self.music_player.playlist.currentIndexChanged.connect(self.do_currentChanged)

        self.netease_panel = NeteaseMusicSearchedPanel()
        self.netease_panel.music_result_list.doubleClicked.connect(self.playClickedMusic)

        self.current_play_list = PlayListPanel('播放历史', '您播放过的音乐')
        self.current_play_list.music_play_list.doubleClicked.connect(self.playClickedMusic)
        self.current_play_list.music_play_list.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)

        # 添加到stack
        self.music_stack.addWidget(MusicPage())
        self.music_stack.addWidget(self.netease_panel)
        self.music_stack.addWidget(self.current_play_list)

        # 添加到主页面
        music_layout = QHBoxLayout()
        music_layout.addWidget(self.music_player)
        music_layout.setSpacing(0)
        music_widget = QWidget()
        music_widget.setLayout(music_layout)
        music_widget.setObjectName("nav_bar")
        music_widget.setStyleSheet("QWidget#nav_bar{border-top: 1px solid lightgrey;background: #ECF1FA !important;}")
        music_widget.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.music_stack)
        self.addWidget(music_widget)

    def playClickedMusic(self):
        # print('当前行：', self.netease_panel.music_result_list.currentRow())
        try:
            music_id = self.sender().selectedItems()[0].whatsThis()
            if music_id not in self.current_play_list.song_ids:
                self.current_play_list.song_ids.insert(0, music_id)
                print(self.current_play_list.song_ids)
                self.getSongThread = getSong(music_id)
                self.getSongThread.song_url.connect(self.updateMusicPlayer)
                self.getSongThread.start()
            else:
                self.music_player.currentMusicId = music_id
                # print(music_id, '歌曲已经在列表中第',self.current_play_list.song_ids.index(self.music_player.currentMusicId), '个位置上了！')
                if self.current_play_list.song_ids.index(self.music_player.currentMusicId) == self.music_player.playlist.currentIndex():
                    if self.music_player.player.state() == QMediaPlayer.PlayingState:
                        self.music_player.player.pause()
                        self.music_player.play_button.setChecked(False)
                        self.music_player.play_button.setIcon(icon('mdi.play', color='#fff'))
                        self.music_player.play_button.setToolTip('播放')
                    elif self.music_player.player.state() == QMediaPlayer.PausedState:
                        self.music_player.player.play()
                        self.music_player.play_button.setChecked(True)
                        self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
                        self.music_player.play_button.setToolTip('暂停')
                else:
                    self.music_player.playlist.setCurrentIndex(self.current_play_list.music_play_list.currentRow())
                    self.music_player.player.play()
                    self.music_player.play_button.setChecked(True)
                    self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
                    self.music_player.play_button.setToolTip('暂停')
        except Exception as e:
            print(e)

    def updateMusicPlayer(self, code, music_url, music_info):
        """
        更新播放器
        :param music_id:
        :param music_url:
        :param music_info:
        :return:
        """
        try:
            if code == 200:
                print(music_url)
                music = {}
                music['id'] = music_info['id']
                music['album'] = music_info['al']['name']
                artist_name = ''
                for artist in music_info['ar']:
                    artist_name = artist_name + str(artist['name']) + '/'
                music['artist'] = artist_name[:-1]
                music['name'] = music_info['name']
                music['pic'] = music_info['al']['picUrl']
                self.current_play_list.music_play_list.add_Music_Tile(music)

                req = requests.get(music['pic'])
                photo = QPixmap()
                photo.loadFromData(req.content)
                photo = photo.scaled(60, 60, Qt.IgnoreAspectRatio)
                self.music_player.music_pic.resize(60, 60)
                self.music_player.music_pic.setPixmap(photo)
                self.music_player.music_window_title.setText(music['name'])
                self.music_player.music_window_author.setText(music['artist'])

                self.music_player.playlist.insertMedia(0, QMediaContent(QUrl(music_url)))
                self.music_player.playlist.setCurrentIndex(0)
                self.current_play_list.music_play_list.setCurrentRow(0)
                print(self.music_player.player.isAvailable())
                if self.music_player.player.isAvailable() == False:
                    print('音乐暂时无法播放')
                    QMessageBox.warning(self, '出错啦', '音乐暂时无法播放', QMessageBox.Yes, QMessageBox.Yes)
                self.music_player.player.play()
                if not self.music_player.play_button.isChecked():
                    self.music_player.player.play()
                    self.music_player.play_button.setChecked(True)
                    self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
                    self.music_player.play_button.setToolTip('暂停')
            else:
                print('音乐暂时无法播放')
                QMessageBox.warning(self, '出错啦', '音乐暂时无法播放', QMessageBox.Yes, QMessageBox.Yes)

        except Exception as e:
            print(e)

    def play_music(self):
        if self.music_player.playlist.currentIndex() < 0:
            self.music_player.playlist.setCurrentIndex(0)
        if self.music_player.play_button.isChecked():
            self.music_player.player.play()
            self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
            self.music_player.play_button.setToolTip('暂停')
        else:
            self.music_player.player.pause()
            self.music_player.play_button.setIcon(icon('mdi.play', color='#fff'))
            self.music_player.play_button.setToolTip('播放')

    def myListWidgetContext(self, point: QPoint):
        item = self.current_play_list.music_play_list.itemAt(point.x(), point.y())
        if item!=None:
            popMenu = QMenu()
            deleteAction = QAction(u'删除', self)
            deleteAction.setIcon(icon('mdi.trash-can-outline'))
            deleteAction.triggered.connect(self.delete_action)

            popMenu.addAction(deleteAction)
            popMenu.addAction(QAction(u'修改', self))
            popMenu.exec_(QCursor.pos())

    def delete_action(self):
        pos = self.current_play_list.music_play_list.currentRow()
        item = self.current_play_list.music_play_list.currentItem()
        self.current_play_list.music_play_list.takeItem(self.current_play_list.music_play_list.row(item))
        if self.music_player.playlist.currentIndex() == pos:
            nextPos = 0
            if pos >= 1:
                nextPos = pos - 1
            self.music_player.playlist.removeMedia(pos)
            if self.current_play_list.music_play_list.count() > 0:
                self.music_player.playlist.setCurrentIndex(nextPos)
                self.do_currentChanged()
            else:
                self.music_player.player.stop()
                self.music_player.play_button.setChecked(False)
                self.music_player.play_button.setIcon(icon('mdi.play', color='#fff'))
                self.music_player.play_button.setToolTip('播放')
                print('无音乐')

        else:
            self.music_player.playlist.removeMedia(pos)

    def do_currentChanged(self):
        newindex = self.music_player.playlist.currentIndex()
        self.current_play_list.music_play_list.setCurrentRow(newindex)

    def next_music(self):
        self.music_player.playlist.next()
        newindex = self.music_player.playlist.currentIndex()
        self.current_play_list.music_play_list.setCurrentRow(newindex)

    def previous_music(self):
        self.music_player.playlist.previous()
        newindex = self.music_player.playlist.currentIndex()
        self.current_play_list.music_play_list.setCurrentRow(newindex)

class MusicPage(CMRichPanel):
    """
    页面内容
    """
    def __init__(self):
        super(MusicPage, self).__init__()

        self.title.setText('音乐')
        self.subTitle.setText('网易云音乐')

    def getCenterLayout(self):
        return centerlize(get_scaled_image('res/svg/#418AE4/music.png', 1))
