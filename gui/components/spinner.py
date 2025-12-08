from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui     import QPixmap, QPainter, QColor
from PyQt6.QtCore    import Qt, QPropertyAnimation, pyqtProperty

from gui.util.svg_icon import QPixmap_from_svg


class Spinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap = QPixmap_from_svg('dots-circle').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.setFixedSize(40, 40)
        self._angle = 0

        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.setDuration(2000)

    def start(self):
        self.animation.start()

    def stop(self):
        self.animation.stop()

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def paintEvent(self, ev=None):
        painter = QPainter(self)

        painter.translate(20, 20)
        painter.rotate(self._angle)
        painter.translate(-20, -20)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()