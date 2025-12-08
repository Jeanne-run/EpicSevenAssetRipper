from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
import os

def _svg_to_icon(img: QPixmap, color='black'):
    qp = QPainter(img)
    qp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    qp.fillRect( img.rect(), QColor(color) )
    qp.end()
    return QIcon(img)

def QPixmap_from_svg(icon_name: str):
    svg_filepath = os.path.join('gui', 'assets', 'icons', icon_name)
    return QPixmap(svg_filepath)

# https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt
def QIcon_from_svg(icon_name: str, color='black'):
    return _svg_to_icon(
        QPixmap_from_svg(icon_name),
        color)