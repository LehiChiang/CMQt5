from PyQt5.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, pyqtSlot, QAbstractAnimation, QSize
from PyQt5.QtWidgets import QWidget, QToolButton, QScrollArea, QSizePolicy, QFrame, QVBoxLayout
from qtawesome import icon


class CMCollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CMCollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        # self.toggle_button.setLayoutDirection(Qt.RightToLeft)
        self.toggle_button.setObjectName('list_label')
        self.toggle_button.setStyleSheet("""
            /*list的标签样式*/
            QToolButton#list_label{
                font-size:15px;
                font-family:Century Gothic;
                padding: .9em .4em .4em .4em;
                color: #333;
                background: #F5F5F7;
                text-align: left;
                border: none;
            }
            """)
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setIcon(icon('fa.angle-down'))
        self.toggle_button.setIconSize(QSize(24, 24))
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setIcon(icon('fa.angle-down') if not checked else icon('fa.angle-right'))
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(100)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)
