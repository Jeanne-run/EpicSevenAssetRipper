from PyQt6.QtWidgets import QDialog, QScrollArea, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore    import Qt

class ScrollableDialogWindow(QDialog):
    '''
        Create a dialog window with 3 sections: Header, Body, Footer

        Body is scrollable
    '''
    def __init__(self, parent = None, title:str='', flags = None):
        super().__init__(parent)

        if not flags:
            self.setWindowFlags(Qt.WindowType.Window |
                Qt.WindowType.CustomizeWindowHint |
                Qt.WindowType.WindowTitleHint)
        else:
            self.setWindowFlags(flags)

        if title: self.setWindowTitle( title )
        self.setMaximumHeight(600)
        self.setMinimumWidth(300)
        self.setMaximumWidth(600)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.header = QWidget(self)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        self.header.setLayout(header_layout)
        self.header.setMinimumHeight(0)
        main_layout.addWidget(self.header)

        #-------- BODY
        self.body_scroll = QScrollArea(self)
        self.body = QWidget(self)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.body.setLayout(self.body_layout)
        
        self.body_scroll.setWidget(self.body)
        self.body_scroll.setWidgetResizable(True)
        main_layout.addWidget(self.body_scroll)


        #-------- FOOTER
        self.footer = QWidget(self)
        footer_layout = QVBoxLayout()
        footer_layout.setContentsMargins(0,0,0,0)
        self.footer.setLayout(footer_layout)
        main_layout.addWidget(self.footer)

        self.show()

    def _clear_part(self, _widget: QWidget):
        '''
            remove everything from this widget except the layout
        '''
        _layout = _widget.layout()

        for item in _widget.children():
            if item != _layout:
                _layout.removeWidget(item)
                item.deleteLater()

    def clear_header(self):
        self._clear_part(self.header)

    def clear_body(self):
        self._clear_part(self.body)

    def clear_footer(self):
        self._clear_part(self.footer)
