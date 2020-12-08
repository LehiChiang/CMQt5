from PyQt5.QtWidgets import QLabel

style = """
/*list的标签样式*/
QLabel#list_label{
    font-size:15px;
    font-family:Century Gothic;
    padding: 1.1em .4em .4em .4em;
    color: #333;
    background: #F5F5F7;
    text-align: left;
    border: none;
}
"""
class CMListLabel(QLabel):
    def __init__(self, text):
        super(CMListLabel, self).__init__()
        self.setText(text)
        self.setObjectName('list_label')
        self.setStyleSheet(style)
