"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: FramelessDialog
@description: 无边框圆角对话框
"""
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, \
    QGraphicsDropShadowEffect, QPushButton, QSpacerItem, \
    QSizePolicy, QLabel, QHBoxLayout

__Author__ = "Irony"
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image

Stylesheet = """
#Custom_Widget {
    background: white;
    border-radius: 10px;
}

#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: #ECF1FA;
}
#content{
    font-size:15px;
    font-family:Century Gothic;
    font-weight: bold;
    margin-left:10px;
    margin-top:5px;
}
"""


class CMDialog(QDialog):

    def __init__(self, title, panel, *args, **kwargs):
        super(CMDialog, self).__init__(*args, **kwargs)
        self.title = title
        self.args = args
        self.panel = panel
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)
        self.setWindowTitle('提示')
        self.initUi()
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def initUi(self):
        layout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout.addWidget(self.widget)


        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel(self.title, objectName='content'))
        top_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(QPushButton('r', self, clicked=self.accept, objectName='closeButton'))

        layout = QVBoxLayout(self.widget)
        layout.addLayout(top_layout)
        layout.addLayout(centerlize(self.panel))

    def sizeHint(self):
        return QSize(600, 400)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
