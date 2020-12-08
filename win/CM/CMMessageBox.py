from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox

Stylesheet = """
#Custom_MessageBox {
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


class CMMessageBox(QMessageBox):

    def __init__(self, *args, **kwargs):
        super(CMMessageBox, self).__init__(*args, **kwargs)
        # self.setObjectName('Custom_MessageBox')
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet(Stylesheet)
        # # self.initUi()
        # # 添加阴影
        # effect = QGraphicsDropShadowEffect(self)
        # effect.setBlurRadius(12)
        # effect.setOffset(0, 0)
        # effect.setColor(Qt.gray)
        # self.setGraphicsEffect(effect)

    # def initUi(self):
    #     layout = QVBoxLayout(self)
    #     self.widget = QWidget(self)
    #     self.widget.setObjectName('Custom_MessageBox')
    #     layout.addWidget(self.widget)
    #
    #     top_layout = QHBoxLayout()
    #     top_layout.addWidget(QLabel('You sure to quit?', objectName='content'))
    #     top_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    #     top_layout.addWidget(QPushButton('r', self, clicked=self.accept, objectName='closeButton'))
    #
    #     layout = QVBoxLayout(self.widget)
    #     layout.addLayout(top_layout)
    #     layout.addLayout(centerlize(get_scaled_image('', 0.2)))

    # def sizeHint(self):
    #     return QSize(600, 400)

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

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CMMessageBox()
    w.exec_()
    QTimer.singleShot(2, app.quit)
    sys.exit(app.exec_())