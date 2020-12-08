from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from qtawesome import icon

style = """
/*主按钮样式*/
#list_button {
    padding: .6em .6em .6em .9em;
    color: #333;
    font-size: 14px;
    font-family: Century Gothic;
    background: #F5F5F7;
    text-align: left;
    border: none;
}
#list_button:hover{
    background: lightblue;
    border-right: 10px red solid;
}
"""
class CMListButton(QPushButton):

    def __init__(self, text, icon_name, *args, **kwargs):
        super(CMListButton, self).__init__(*args, **kwargs)
        self.setText(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIcon(icon(icon_name, color='grey', color_active='#418AE4'))
        self.setIconSize(QSize(24, 24))
        self.setObjectName('list_button')
        self.setStyleSheet(style)
        self.resize(self.sizeHint())
