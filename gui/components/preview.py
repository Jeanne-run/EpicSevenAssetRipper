from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea
from PyQt6.QtGui     import QPixmap

from typing          import Literal

class FileContentPreview(QWidget):
    previewedWidget: QPixmap | QLabel = None

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        
        # Buttons
        header_widget = QWidget()
        hLine = QHBoxLayout()
        header_widget.setLayout(hLine)
        self.layout().addWidget(header_widget)
        text = QLabel(text='Preview')
        hLine.addWidget(text)

        close = QPushButton()
        close.setText('x')
        close.setFixedWidth(25)
        close.clicked.connect(lambda: self.setHidden(True))
        hLine.addWidget(close)

        self.scrollWidget = QScrollArea()
        self.layout().addWidget(self.scrollWidget)


    def display(self, type: Literal['image', 'text', 'byte'], content: bytearray | bytes | str):
        if self.previewedWidget:
            self.previewedWidget.deleteLater()

        try:
            match type:
                case 'image':
                    wid = QLabel()
                    image = QPixmap()
                    image.loadFromData(content)
                    wid.setPixmap(image)
                    wid.setScaledContents(True)
                    self.scrollWidget.setWidget(wid)
                    self.previewedWidget = wid
        except Exception as e:
            wid = QLabel()
            wid.setText(f'Preview error: {e}')
            self.scrollWidget.setWidget(wid)

