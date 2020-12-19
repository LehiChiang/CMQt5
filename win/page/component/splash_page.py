# -*-coding:utf-8-*-
import time
from sys import argv

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QImage, QCursor
from PyQt5.QtWidgets import QSplashScreen, QApplication, QLabel, QVBoxLayout, QDesktopWidget

from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class SplashPanel(QSplashScreen):
    def __init__(self):
        super(SplashPanel, self).__init__()
        self.m_flag = False
        self.widthRatio = 0.45
        self.heightRatio = 0.45
        desktop = QApplication.desktop()
        self.winWidth = desktop.width()
        self.winHeight = desktop.height()
        self.screenWidth = self.winWidth * self.widthRatio
        self.screenHeight = self.winHeight * self.heightRatio
        self.size = QSize(self.screenWidth, self.screenHeight)
        self.resize(self.size)
        self.main_layout = QVBoxLayout()
        self.logo_label = get_scaled_image('res/gummy-city.svg', 0.4)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(centerlize(self.logo_label))
        self.main_layout.addStretch(1)
        self.load_label = QLabel('加载中')
        self.main_layout.addWidget(self.load_label, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)
        self.setStyleSheet('background-color:#ECF1FA;')
        # self.setAttribute(Qt.WA_TranslucentBackground)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()
        for i in range(1, 5):
            self.load_label.setText('正在加载资源{}'.format('.' * i))
            time.sleep(0.15)

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


if __name__ == '__main__':
    app = QApplication(argv)
    splash = SplashPanel()
    exit(app.exec_())
