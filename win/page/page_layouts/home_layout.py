from PyQt5.QtWidgets import QVBoxLayout

from win.CM.CMDialog import CMDialog
from win.CM.CMRichPanel import CMRichPanel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class HomePageLayout(QVBoxLayout):
    """
    页面内容的layout，传入page
    """
    def __init__(self):
        super(HomePageLayout, self).__init__()
        self.addWidget(HomePage())


class HomePage(CMRichPanel):
    """
    页面内容
    """
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)

        self.title.setText('Welcome to CMQt5!')
        self.subTitle.setText('A powerful, beautiful, fast PyQt5 framework for instant desktop application development '
                              'toolkit.')

    def getCenterLayout(self):
        return centerlize(get_scaled_image('res/svg/#418AE4/welcome.png', 1))