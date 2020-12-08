from sys import argv, exit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QMainWindow, QHBoxLayout, \
    QStackedWidget
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent
from qtawesome import icon

from service.CommomHelper import CommonHelper
from win.CM.CMInputBox import CMInputBox
from win.CM.CMMessageBox import CMMessageBox
from win.page.basic.blank import BlankPage

from win.page.component.button_group import TopRightButtonGroup
from win.page.component.outer_list import OuterPanel
from win.page.page_layouts.chart_layout import ChartPageLayout
from win.page.page_layouts.home_layout import HomePageLayout
from win.page.basic.splitter import SplitterPage
from win.page.page_layouts.music_layout import MusicPageLayout
from win.page.page_layouts.music_list_layout import MusicListPageLayout
from win.page.page_layouts.setting_layout import SettingPageLayout


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.widthRatio = 0.75
        self.heightRatio = 0.75
        desktop = QApplication.desktop()
        self.winWidth = desktop.width()
        self.winHeight = desktop.height()
        self.screenWidth = self.winWidth * self.widthRatio
        self.screenHeight = self.winHeight * self.heightRatio
        self.initAppBar()
        self.initCenterWidget()
        self.initUI()

        # self.main_layout.addWidget(self.appbar)
        self.main_layout.addLayout(self.stackLayout)

    def initAppBar(self):
        self.appbar = QWidget()
        self.appbar.setFixedHeight(60)
        self.appbar_main_layout = QHBoxLayout(self.appbar)
        self.top_right_btn_group = TopRightButtonGroup()
        self.top_right_btn_group.left_close.clicked.connect(self.close)
        self.top_right_btn_group.left_visit.clicked.connect(self.windowMaximize)
        self.top_right_btn_group.left_mini.clicked.connect(self.windowMinimize)
        self.search_box = CMInputBox(placeholder='Search', shadow=False, icon=icon('fa.search', color='#fff'))
        self.appbar_main_layout.addStretch(1)
        self.appbar_main_layout.addWidget(self.search_box)
        self.appbar_main_layout.addStretch(4)
        self.appbar_main_layout.addWidget(self.top_right_btn_group)
        self.appbar.setObjectName('app_bar')

    def initCenterWidget(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)

        # 添加左侧功能区
        self.outer_panel = OuterPanel()
        self.outer_panel.outer_list.currentRowChanged.connect(self.display)
        self.outer_list_panel = QWidget()
        self.outer_list_panel.setFixedWidth(56)
        self.outer_list_panel.setObjectName('outer_left_widget')
        self.outer_list_panel.setLayout(self.outer_panel)

        # 添加stack
        self.main_stack = QStackedWidget(self.outer_list_panel)
        self.main_stack.addWidget(BlankPage(HomePageLayout()))
        self.main_stack.addWidget(SplitterPage(QVBoxLayout(), ChartPageLayout()))
        self.musicpagelayout = MusicPageLayout()
        self.main_stack.addWidget(SplitterPage(MusicListPageLayout(self.musicpagelayout), self.musicpagelayout))
        self.main_stack.addWidget(BlankPage(SettingPageLayout()))

        # 下方主体为水平布局
        self.stackLayout = QHBoxLayout()
        self.stackLayout.addWidget(self.outer_list_panel)
        self.stackLayout.addWidget(self.main_stack)

    def initUI(self):
        self.setCentralWidget(self.main_widget)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.resize(int(self.screenWidth), int(self.screenHeight))
        # self.setWindowTitle('CM工具箱')
        self.setWindowIcon(QIcon('res/setting.png'))
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        # self.effect_shadow = QGraphicsDropShadowEffect(self)
        # self.effect_shadow.setOffset(0, 0)
        # self.effect_shadow.setBlurRadius(15)
        # self.effect_shadow.setColor(Qt.gray)
        # self.main_widget.setGraphicsEffect(self.effect_shadow)

    def display(self, i):
        self.main_stack.setCurrentIndex(i)

    def closeEvent(self, event):
        reply = CMMessageBox.question(self, '消息',
                                      "你确定要退出吗？", CMMessageBox.Yes |
                                      CMMessageBox.No, CMMessageBox.No)
        if reply == CMMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def windowMaximize(self):
        if self.windowState() == Qt.WindowNoState:
            self.setWindowState(Qt.WindowMaximized)
        elif self.windowState() == Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)

    def windowMinimize(self):
        self.setWindowState(Qt.WindowMinimized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, a0: QMouseEvent):
        self.windowMaximize()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(argv)
    app.setApplicationDisplayName('CM工具箱')
    app.setApplicationVersion('1.0.1')
    win = MainWindow()
    styleFile = 'res/style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    win.show()
    win.setStyleSheet(qssStyle)
    exit(app.exec_())
