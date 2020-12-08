from PyQt5.QtWidgets import QSplitter, QWidget, QApplication, QVBoxLayout, QLayout

from win.page.page_layouts.music_list_layout import MusicListPageLayout


class SplitterPage(QSplitter):
    """
    page页面，接受layout参数
    """
    def __init__(self, left_layout: QLayout, right_layout: QLayout):
        super(SplitterPage, self).__init__()
        self.left_widget = self.get_left_widget()
        self.right_widget = self.get_right_widget()

        self.left_layout = left_layout
        self.right_layout = right_layout
        self.right_layout.setSpacing(0)

        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)

        self.addWidget(self.left_widget)
        self.addWidget(self.right_widget)
        self.initUI()

    def initUI(self):
        self.setHandleWidth(1)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 4)
        self.setCollapsible(0, False)
        self.setCollapsible(1, False)

    def get_left_widget(self):
        left_widget = QWidget()
        left_widget.setMaximumWidth(300)
        left_widget.setMinimumWidth(200)
        left_widget.setObjectName('left_widget')
        left_widget.setStyleSheet("QWidget#left_widget{background: #F5F5F7 !important;}")
        return left_widget

    def get_right_widget(self):
        right_widget = QWidget()
        right_widget.setObjectName('right_widget')
        # right_widget.setContentsMargins(0, 0, 0, 0)         border-bottom-right-radius: 5px;
        right_widget.setStyleSheet("QWidget#right_widget{background: #fff;}")
        right_widget.setContentsMargins(0, 0, 0, 0)
        return right_widget


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    page = SplitterPage(MusicListPageLayout(), QVBoxLayout())
    page.resize(640, 480)
    page.show()
    exit(app.exec_())