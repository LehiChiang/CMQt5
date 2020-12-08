from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


def centerlize(widget: QWidget):
    vbox = QVBoxLayout()
    vbox.addStretch(1)
    vbox.addWidget(widget)
    vbox.addStretch(1)
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addLayout(vbox)
    hbox.addStretch(1)
    return hbox