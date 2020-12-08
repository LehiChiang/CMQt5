from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLayout


class BlankPage(QWidget):
    """
    page页面，接受layout参数                                border-bottom-right-radius: 5px;
    """
    def __init__(self, widget_layout: QLayout):
        super(BlankPage, self).__init__()
        self.widget_layout = widget_layout

        self.panel = QWidget()
        self.panel.setLayout(self.widget_layout)
        self.panel.setObjectName('blank_page')
        self.panel.setStyleSheet("QWidget#blank_page {background: #fff;}")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.panel)
        self.setLayout(self.layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    page = BlankPage(QVBoxLayout())
    page.show()
    exit(app.exec_())

