from PyQt5.QtWidgets import QVBoxLayout

from win.CM.CMRichPanel import CMRichPanel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class SettingPageLayout(QVBoxLayout):
    """
    页面内容的layout，传入page
    """
    def __init__(self):
        super(SettingPageLayout, self).__init__()
        self.addWidget(SettingPage())


class SettingPage(CMRichPanel):
    """
    页面内容
    """
    def __init__(self):
        super(SettingPage, self).__init__()

        self.title.setText('Setting')
        self.subTitle.setText('Modify the settings according to your preferences.')

    def buttonClick(self):
        print('Saved!')

    def getCenterLayout(self):
        return centerlize(get_scaled_image('res/svg/#418AE4/setting.png', 1))
