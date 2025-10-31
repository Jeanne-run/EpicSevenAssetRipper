from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
import os

# https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt
def QIcon_from_svg(icon_name: str, color='black'):
    svg_filepath = os.path.join('gui', 'assets', 'icons', icon_name)
    img = QPixmap(svg_filepath)
    qp = QPainter(img)
    qp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    qp.fillRect( img.rect(), QColor(color) )
    qp.end()
    return QIcon(img)