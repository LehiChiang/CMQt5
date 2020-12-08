from PyQt5.QtWidgets import QVBoxLayout

from win.CM.CMRichPanel import CMRichPanel
from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class ChartPageLayout(QVBoxLayout):
    """
    页面内容的layout，传入page
    """
    def __init__(self):
        super(ChartPageLayout, self).__init__()
        self.addWidget(ChartPage())


class ChartPage(CMRichPanel):
    """
    页面内容
    """
    def __init__(self):
        super(ChartPage, self).__init__()

        self.title.setText('数据可视化')
        self.subTitle.setText('这里使用科学计算图形库的展示作为机器学习项目数据可视化的第一步！')

    def getCenterLayout(self):
        return centerlize(get_scaled_image('res/svg/#418AE4/data_vis.png', 1))
