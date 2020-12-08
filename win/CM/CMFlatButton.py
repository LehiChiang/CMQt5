from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class CMFlatButton(QPushButton):

    def __init__(self, text, *args, **kwargs):
        super(CMFlatButton, self).__init__(*args, **kwargs)
        self.setText(text)
        self.effect_shadow = QGraphicsDropShadowEffect()
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(15)  # 阴影半径
        self.effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setObjectName('main')
        self.setStyleSheet(self.css())
        self.resize(self.sizeHint())

    def css(self):
        style = """
        /*主按钮样式*/
        #main {
            padding: .6em 1.6em;
            color: #fff;
            border-radius: 23px;
            background: #418AE4;
            box-shadow: 0 2px 5px rgba(0,0,0,.3);
            cursor: pointer;
            font-size:17px;
            font-family:Century Gothic;
        }
        """
        return style
