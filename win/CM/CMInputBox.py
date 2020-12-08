from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QFont, QCursor, QFocusEvent
from PyQt5.QtWidgets import QLineEdit, QAction, QGraphicsDropShadowEffect
import qtawesome


class CMInputBox(QLineEdit):
    def __init__(self, **kwargs):
        super(CMInputBox, self).__init__()
        self.effect_shadow = QGraphicsDropShadowEffect()
        self.leading_icon = qtawesome.icon('fa.search', color='#fff')
        self.leading = QAction(icon=self.leading_icon)
        self.initSetting(kwargs)
        self.initUI()

    def initSetting(self, kwargs):
        if 'text' in kwargs.keys():
            self.setText(kwargs['text'])
        if 'placeholder' in kwargs.keys():
            self.setPlaceholderText(kwargs['placeholder'])
        if 'shadow' in kwargs.keys() and kwargs['shadow']:
            self.effect_shadow.setOffset(0, 0)
            self.effect_shadow.setBlurRadius(10)
            self.effect_shadow.setColor(Qt.gray)
            self.setGraphicsEffect(self.effect_shadow)
        if 'icon' in kwargs.keys():
            self.leading_icon = kwargs['icon']
            self.leading.setIcon(self.leading_icon)
        if 'color' in kwargs.keys():
            self.color = kwargs['color']
        else:
            self.color = '#fff'

    def initUI(self):
        self.styleStr = """
            #lineedit{
                color: %s;
                padding: 7px 2px;
                border: none;
                line-height: 11px;
                border-radius: 4px;
                background: rgb(103,103,103,45);
            }
            #lineedit:focus{
                border: 1px solid #ebebeb;
            }
        """ % self.color
        self.setObjectName('lineedit')
        self.setFont(QFont('微软雅黑', 11))
        self.setStyleSheet(self.styleStr)
        # self.setFocusPolicy(Qt.NoFocus)
        self.setClearButtonEnabled(True)
        self.setDragEnabled(True)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.setCursor(QCursor(Qt.IBeamCursor))
        self.setMaximumWidth(400)
        self.setMinimumWidth(300)
        self.addAction(self.leading, QLineEdit.LeadingPosition)


