from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout

from win.generator.centerlize import centerlize
from win.generator.scaled_image import get_scaled_image


class CMTabs(QTabWidget):
    def __init__(self,parent=None):
        super(CMTabs, self).__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.setMovable(True)
        self.setElideMode(Qt.ElideMiddle)
        self.setCurrentIndex(0)

        # optitle = QtWidgets.QGraphicsOpacityEffect()
        # optitle.setOpacity(0.5)
        # self.setGraphicsEffect(optitle)
        self.tab1UI()
        self.tab2UI()


    def tab1UI(self):
        self.tab1.setLayout(centerlize(get_scaled_image('res/svg/#418AE4/welcome.png', 1)))

    def tab2UI(self):
        self.tab2.setLayout(centerlize(QLabel('Powerful & Beautiful!', font=QFont('Century Gothic', 20))))

