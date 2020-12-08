from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt

def get_scaled_image(img_path: str, ratio: float):
    Img = QLabel()
    img = QImage(img_path)  # 创建图片实例
    mgnWidth = int(img.width() * ratio)
    mgnHeight = int(img.height() * ratio)  # 缩放宽高尺寸
    size = QSize(mgnWidth, mgnHeight)
    pixImg = QPixmap.fromImage(
        img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
    Img.resize(mgnWidth, mgnHeight)
    Img.setPixmap(pixImg)
    return Img


def get_fixed_image(img_path: str, width=170, height=170):
    Img = QLabel()
    Img.setStyleSheet('margin:6px;')
    effect_shadow = QGraphicsDropShadowEffect()
    effect_shadow.setOffset(0, 0)
    effect_shadow.setBlurRadius(20)
    effect_shadow.setColor(Qt.black)
    Img.setGraphicsEffect(effect_shadow)
    img = QImage(img_path)  # 创建图片实例
    size = QSize(width, height)
    pixImg = QPixmap.fromImage(
        img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
    Img.resize(width, height)
    Img.setPixmap(pixImg)
    return Img