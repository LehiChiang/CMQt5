from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QGraphicsDropShadowEffect, QVBoxLayout, QWidget, QHBoxLayout, QLabel, \
    QSpacerItem, QPushButton, QSizePolicy, QDialog, QStyleFactory

from win.CM.CMFlatButton import CMFlatButton
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image

Stylesheet = """
#Custom_MessageBox {
    background: white;
    border-radius: 5px;
}

#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 5px;
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


class CMMessageBox(QDialog):

    def __init__(self, title, msg, *args, **kwargs):
        super(CMMessageBox, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_MessageBox')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)
        self.title = title
        self.msg = msg
        self.close_button = QPushButton('关闭')
        self.cancel_button = QPushButton('取消')
        self.initUi()
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def initUi(self):
        layout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_MessageBox')
        layout.addWidget(self.widget)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel(self.title, objectName='content'))
        top_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(QPushButton('r', self, clicked=self.accept, objectName='closeButton'))

        layout = QVBoxLayout(self.widget)
        layout.addLayout(top_layout)
        layout.addLayout(centerlize(QLabel(self.msg, objectName='content')))

        bottom_layout = QHBoxLayout()
        self.close_button.setStyle(QStyleFactory.create('fusion'))
        self.cancel_button.setStyle(QStyleFactory.create('fusion'))
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.close_button)
        bottom_layout.addWidget(self.cancel_button)
        layout.addLayout(bottom_layout)

    def sizeHint(self):
        return QSize(350, 240)

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