import json
from PyQt5.QtCore import Qt, QSize, QModelIndex
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QListView, QVBoxLayout, QToolButton
from qtawesome import icon


class OuterList(QListWidget):
    def __init__(self):
        super(OuterList, self).__init__()

        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setDragEnabled(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setCursor(Qt.PointingHandCursor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName('fun')
        self.setViewportMargins(0, 0, 0, 0)
        self.setItemAlignment(Qt.AlignCenter)

        with open('config/outer_list_menu.json', 'r', encoding='utf8') as f:
            menu_config = json.load(f)
            self.menu_list = menu_config['menu']

        for menu in self.menu_list:
            self.item = QListWidgetItem()
            self.item.setToolTip(menu['tooltip'])
            self.item.setIcon(icon(menu['icon'], color='grey', color_active='#418AE4', options=[{'active': menu['icon_active']}]))
            self.addItem(self.item)

        self.setCurrentRow(0)
        self.setFixedHeight(self.count() * 55)


class OuterPanel(QVBoxLayout):
    def __init__(self):
        super(OuterPanel, self).__init__()

        self.setAlignment(Qt.AlignHCenter)
        self.outer_list = OuterList()
        self.setting_btn = QToolButton()
        self.setting_btn.setIcon(icon('fa.apple', color='grey', color_active='#418AE4'))
        self.setting_btn.setObjectName('outer_btn')
        self.setting_btn.setStyleSheet("""
            #outer_btn{
                background-color:transparent;
                border:none;
                margin-left: 4px;
            }
        """)
        self.setting_btn.setIconSize(QSize(28, 28))
        self.setting_btn.setToolTip('更多')

        self.addWidget(self.outer_list)
        self.addStretch(1)
        self.addWidget(self.setting_btn)



