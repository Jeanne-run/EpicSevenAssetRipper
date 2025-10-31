from PyQt6.QtWidgets import QDialog, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore    import Qt

class ScrollableDialogWindow(QDialog):
    main_content_area: QVBoxLayout = None
    addWidget: QVBoxLayout.addWidget = None

    def __init__( self, parent = None, window_title = None ):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint)
        
        if window_title:
            self.setWindowTitle(window_title)

        self_layout = QHBoxLayout()
        self.setLayout(self_layout)
        scroll = QScrollArea()
        self.widget = QWidget()
        scroll.setWidget(self.widget)
        self.main_content_area = QVBoxLayout()
        self.widget.setLayout(self.main_content_area)
        self_layout.addWidget(scroll)
        self.addWidget = self.main_content_area.addWidget

        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(1000)

        self.show()

    # def addWidget(self, widget):
    #     self.main_content_area.addWidget(widget)

