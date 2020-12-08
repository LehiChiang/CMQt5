from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class CMCircleButton(QPushButton):

    def __init__(self, radius, *args, **kwargs):
        super(CMCircleButton, self).__init__(*args, **kwargs)
        self.effect_shadow = QGraphicsDropShadowEffect()
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setObjectName('music_play_btn')
        self.setStyleSheet(self.css())
        self.setFixedSize(int(2 * radius), int(2 * radius))
        self.setIconSize(QSize(int(2 * radius) - 10, int(2 * radius) - 10))
        self.setCheckable(True)

    def css(self):
        style = """
        QPushButton#music_play_btn{
            border: none;
            border-radius: 20px;
            background-color: #418AE4;
        }
        """
        return style
