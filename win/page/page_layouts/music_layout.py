import requests
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QHBoxLayout, QWidget, QMessageBox, QMenu, QAction
from qtawesome import icon

from thread.music.Netease.getSongThread import getSong
from win.CM.CMDrawer import CMDrawer
from win.CM.CMRichPanel import CMRichPanel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image
from win.page.component.music.music_navigation_bar import MusicPlayer
from win.page.component.music.netease.netease_music_panel import NeteaseMusicSearchedPanel
from win.page.component.music.play_list_drawer import PlayListDrawerWidget
from win.page.component.music.play_list_panel import PlayListPanel


class MusicPageLayout(QVBoxLayout):
    """
    页面内容的layout，传入page
    """

    def __init__(self, music_play_list):
        super(MusicPageLayout, self).__init__()
        self.music_stack = QStackedWidget()
        self.music_stack.setContentsMargins(10, 10, 10, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        # 歌单信息
        self.music_play_list = music_play_list

        # 播放列表抽屉
        self.right_drawer_widget = PlayListDrawerWidget()
        self.rightDrawer = CMDrawer(self.music_stack, widget=self.right_drawer_widget)
        self.rightDrawer.setDirection(CMDrawer.RIGHT)
        self.right_drawer_widget.music_play_list.doubleClicked.connect(self.play_clicked_music)
        self.right_drawer_widget.music_play_list.customContextMenuRequested[QPoint].connect(self.playlist_popup_context)
        self.right_drawer_widget.top_clear_btn.clicked.connect(self.clear_playlist)

        # 音乐播放导航栏
        self.music_player = MusicPlayer()
        self.music_player.setContentsMargins(0, 0, 0, 0)
        self.music_player.playlist_btn.clicked.connect(self.rightDrawer.show)
        self.music_player.play_button.clicked.connect(self.play_music)
        self.music_player.previous_button.clicked.connect(self.previous_music)
        self.music_player.next_button.clicked.connect(self.next_music)
        self.music_player.playlist.currentIndexChanged.connect(self.do_current_changed)

        self.netease_panel = NeteaseMusicSearchedPanel()
        self.netease_panel.music_result_list.doubleClicked.connect(self.play_clicked_music)
        self.netease_panel.music_result_list.customContextMenuRequested[QPoint].connect(
            self.music_search_list_popup_context)

        # 添加到stack
        self.music_stack.addWidget(MusicPage())
        self.music_stack.addWidget(self.netease_panel)
        for play_list in self.music_play_list:
            self.music_stack.addWidget(PlayListPanel(play_list['list_name'], play_list['list_description']))

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

    def play_clicked_music(self):
        """
        播放点击的音乐
        :return:
        """
        try:
            music_id = self.sender().selectedItems()[0].whatsThis()
            if music_id not in self.right_drawer_widget.song_ids:
                self.right_drawer_widget.song_ids.insert(0, music_id)
                print('当前播放列表：', self.right_drawer_widget.song_ids)
                self.getSongThread = getSong(music_id)
                self.getSongThread.song_url.connect(self.update_music_player)
                self.getSongThread.start()
            else:
                self.music_player.currentMusicId = music_id
                if self.right_drawer_widget.song_ids.index(
                        self.music_player.currentMusicId) == self.music_player.playlist.currentIndex():
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
                    self.music_player.playlist.setCurrentIndex(self.right_drawer_widget.music_play_list.currentRow())
                    self.music_player.player.play()
                    self.music_player.play_button.setChecked(True)
                    self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
                    self.music_player.play_button.setToolTip('暂停')
        except Exception as e:
            print(e)

    def update_music_player(self, music_id, music_url, music_info):
        """
        更新播放器
        :param music_id:
        :param music_url:
        :param music_info:
        :return:
        """
        try:
            if music_url:
                music = {'id': music_info['id'], 'album': music_info['al']['name'], 'name': music_info['name'],
                         'pic': music_info['al']['picUrl']}
                artist_name = ''
                for artist in music_info['ar']:
                    artist_name = artist_name + str(artist['name']) + '/'
                music['artist'] = artist_name[:-1]

                secs = music_info['dt'] / 1000
                mins = secs / 60
                secs = secs % 60
                music['duration'] = "%d:%d" % (mins, secs)

                self.right_drawer_widget.music_play_list.add_music_tile(music)
                self.music_player.playlist.insertMedia(0, QMediaContent(QUrl(music_url)))
                self.music_player.playlist.setCurrentIndex(0)
                self.right_drawer_widget.music_play_list.setCurrentRow(0)
                if not self.music_player.player.isAvailable():
                    print('音乐暂时无法播放')
                    QMessageBox.warning(self.music_stack, '出错啦', '音乐暂时无法播放', QMessageBox.Yes, QMessageBox.Yes)
                self.music_player.player.play()
                if not self.music_player.play_button.isChecked():
                    self.music_player.player.play()
                    self.music_player.play_button.setChecked(True)
                    self.music_player.play_button.setIcon(icon('mdi.pause', color='#fff'))
                    self.music_player.play_button.setToolTip('暂停')
            else:
                print('音乐暂时无法播放')
                self.right_drawer_widget.song_ids.remove(music_id)
                QMessageBox.warning(self.music_stack, '出错啦', '音乐暂时无法播放', QMessageBox.Yes, QMessageBox.Yes)

        except Exception as e:
            print(e)

    def play_music(self):
        if self.music_player.playlist.isEmpty():
            self.music_player.play_button.setChecked(False)
            return
        else:
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

    def playlist_popup_context(self, point: QPoint):
        """
        播放列表的右键菜单
        :param point:
        :return:
        """
        item = self.right_drawer_widget.music_play_list.itemAt(point.x(), point.y())
        if item:
            pop_menu = QMenu()
            delete_action = QAction(u'删除', self)
            delete_action.setIcon(icon('mdi.trash-can-outline'))
            delete_action.triggered.connect(self.delete_action)

            pop_menu.addAction(delete_action)
            pop_menu.addAction(QAction(u'修改', self))
            pop_menu.exec_(QCursor.pos())

    def music_search_list_popup_context(self, point: QPoint):
        """
        音乐搜索结果的右键菜单
        :param point:
        :return:
        """
        item = self.netease_panel.music_result_list.itemAt(point.x(), point.y())
        if item:
            pop_menu = QMenu()
            add_play_action = QAction(u'添加到播放列表', self)
            add_play_action.setIcon(icon('mdi.playlist-plus'))
            add_play_action.triggered.connect(self.add_music_action)

            download_music_action = QAction(u'下载', self)
            download_music_action.setIcon(icon('mdi.download'))
            download_music_action.triggered.connect(self.download_music_action)

            pop_menu.addAction(add_play_action)
            pop_menu.addSeparator()
            pop_menu.addAction(download_music_action)
            pop_menu.exec_(QCursor.pos())

    def add_music_action(self):
        print('hello')

    def download_music_action(self):
        print('download')

    def delete_action(self):
        """
        删除音乐项
        :return:
        """
        pos = self.right_drawer_widget.music_play_list.currentRow()
        item = self.right_drawer_widget.music_play_list.currentItem()
        self.right_drawer_widget.music_play_list.takeItem(self.right_drawer_widget.music_play_list.row(item))
        self.right_drawer_widget.song_ids.remove(item.whatsThis())
        if self.music_player.playlist.currentIndex() == pos:
            next_pos = 0
            if pos >= 1:
                next_pos = pos - 1
            self.music_player.playlist.removeMedia(pos)
            if self.right_drawer_widget.music_play_list.count() > 0:
                self.music_player.playlist.setCurrentIndex(next_pos)
                self.do_current_changed()
            else:
                self.music_player.player.stop()
                self.music_player.play_button.setChecked(False)
                self.music_player.play_button.setIcon(icon('mdi.play', color='#fff'))
                self.music_player.play_button.setToolTip('播放')
                print('无音乐')

        else:
            self.music_player.playlist.removeMedia(pos)

    def do_current_changed(self):
        """
        播放列表切换时触发的事件
        :return:
        """
        new_index = self.music_player.playlist.currentIndex()
        self.getSongThread = getSong(self.right_drawer_widget.song_ids[new_index])
        self.getSongThread.song_url.connect(self.update_music_window_tile)
        self.getSongThread.start()
        self.right_drawer_widget.music_play_list.setCurrentRow(new_index)

    def update_music_window_tile(self, music_id, music_url, music_info):
        """
        更新音乐的海报窗口
        :return:
        """
        if music_url:
            music = {'id': music_info['id'], 'album': music_info['al']['name'], 'name': music_info['name'],
                     'pic': music_info['al']['picUrl']}
            artist_name = ''
            for artist in music_info['ar']:
                artist_name = artist_name + str(artist['name']) + '/'
            music['artist'] = artist_name[:-1]
            secs = music_info['dt'] / 1000
            mins = secs / 60
            secs = secs % 60
            music['duration'] = "%d:%d" % (mins, secs)

            req = requests.get(music['pic'])
            photo = QPixmap()
            photo.loadFromData(req.content)
            photo = photo.scaled(60, 60, Qt.IgnoreAspectRatio)
            self.music_player.music_pic.resize(60, 60)
            self.music_player.music_pic.setPixmap(photo)
            self.music_player.music_window_title.setText(music['name'])
            self.music_player.music_window_author.setText(music['artist'])

    def next_music(self):
        """
        前一首歌切换
        :return:
        """
        self.music_player.playlist.next()
        new_index = self.music_player.playlist.currentIndex()
        self.right_drawer_widget.music_play_list.setCurrentRow(new_index)

    def previous_music(self):
        """
        下一首歌切换
        :return:
        """
        self.music_player.playlist.previous()
        new_index = self.music_player.playlist.currentIndex()
        self.right_drawer_widget.music_play_list.setCurrentRow(new_index)

    def clear_playlist(self):
        self.right_drawer_widget.music_play_list.clear()
        self.right_drawer_widget.song_ids.clear()
        self.music_player.playlist.clear()
        self.music_player.player.stop()
        self.music_player.play_button.setChecked(False)
        self.music_player.play_button.setIcon(icon('mdi.play', color='#fff'))
        self.music_player.play_button.setToolTip('播放')
        print('无音乐')

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
