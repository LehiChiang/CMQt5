from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QToolButton, QHBoxLayout
from qtawesome import icon


class TopRightButtonGroup(QWidget):
    def __init__(self):
        super(TopRightButtonGroup, self).__init__()
        self.left_close = QToolButton()
        self.left_visit = QToolButton()
        self.left_mini = QToolButton()
        self.left_close.setIcon(icon('fa.times', color='#fff'))
        self.left_close.setIconSize(QSize(22, 22))
        self.left_close.setObjectName('left_close')
        self.left_close.setToolTip('关闭程序')
        self.left_close.setCursor(QCursor(Qt.PointingHandCursor))
        self.left_visit.setIcon(icon('fa5.square', color='#fff'))
        self.left_visit.setIconSize(QSize(20, 20))
        self.left_visit.setObjectName('left_visit')
        self.left_visit.setToolTip('最大化界面')
        self.left_visit.setCursor(QCursor(Qt.PointingHandCursor))
        self.left_mini.setIcon(icon('fa5s.minus', color='#fff'))
        self.left_mini.setIconSize(QSize(20, 20))
        self.left_mini.setObjectName('left_mini')
        self.left_mini.setToolTip('最小化界面')
        self.left_mini.setCursor(QCursor(Qt.PointingHandCursor))
        self.top_right_btn_group = QHBoxLayout()
        self.top_right_btn_group.addWidget(self.left_mini)
        self.top_right_btn_group.addWidget(self.left_visit)
        self.top_right_btn_group.addWidget(self.left_close)
        self.setLayout(self.top_right_btn_group)
