from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from win.CM.CMFlatButton import CMFlatButton

style = """
#tablabel{
    padding: 5px 0px 5px 0px;
}
#tabsublabel{
    padding: 10px 0px;
    color: grey;
}
"""
class CMRichPanel(QWidget):
    """
    title, subTitle, centerWidget, btn, statusBar
    """
    def __init__(self,parent=None):
        super(CMRichPanel, self).__init__(parent)

        #最上方
        self.title = QLabel('Welcome to CMQt5!', font=QFont('黑体', 20))
        self.title.setObjectName('tablabel')
        self.title.setStyleSheet(style)
        self.subTitle = QLabel('A powerful, beautiful, fast PyQt5 framework for instant desktop application development '
            'toolkit.', font=QFont('黑体', 12))
        self.subTitle.setObjectName('tabsublabel')
        self.subTitle.setStyleSheet(style)

        #status状态栏
        self.showStatusBar = self.showStatusBar()

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.subTitle)
        if self.getCenterLayout():
            self.vbox.addLayout(self.getCenterLayout())
        if self.showStatusBar:
            self.statusBar = QHBoxLayout()
            self.statusBar.setObjectName('statusbar')
            self.statusInfo = QLabel('Status Information')
            self.statusBar.addWidget(self.statusInfo)
            self.statusInfo.setStyleSheet('font-family:微软雅黑;color: grey;')
            self.vbox.addLayout(self.statusBar)

    def getCenterLayout(self):
        return None

    def showStatusBar(self):
        return False
