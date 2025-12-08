from PyQt6.QtWidgets   import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore      import pyqtSignal, Qt, QEvent
from gui.util.svg_icon import QIcon_from_svg

class SearchBar(QWidget):
    # Emits only after the Enter key is pressed
    search = pyqtSignal(str)
    # Emits after each key press
    typing = pyqtSignal(str)

    def __init__(self, parent=None, placeholder=None):
        super().__init__(parent)

        THEME_COLORS = QApplication.instance().ThemeColors

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        self.setMinimumWidth(100)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText(placeholder)
        self.input_field.setFixedHeight(30)
        self.input_field.setContentsMargins(0, 0, 0, 0)
        self.input_field.installEventFilter(self.input_field)
        self.input_field.eventFilter = self.eventFilter
        self.input_field.setStyleSheet(f'background-color: {THEME_COLORS.INPUT_BACKGROUND_COLOR}; color {THEME_COLORS.INPUT_FONT_COLOR}; border-top-left-radius: {THEME_COLORS.INPUT_BORDER_RADIUS}px; border-bottom-left-radius: {THEME_COLORS.INPUT_BORDER_RADIUS}px; border-top-right-radius: 0; border-bottom-right-radius: 0; border: {THEME_COLORS.INPUT_BORDER_WIDTH}px solid {THEME_COLORS.INPUT_BORDER_COLOR}; border-right: none;')
        layout.addWidget(self.input_field)
        layout.setStretchFactor(self.input_field, 1)

        self.go_button = QPushButton(self)
        self.go_button.setIcon(QIcon_from_svg('magnify.svg', THEME_COLORS.INPUT_ICON_COLOR))
        self.go_button.setFixedHeight(30)
        self.go_button.setMinimumWidth(20)
        self.go_button.setContentsMargins(0, 0, 0, 0)
        self.go_button.setStyleSheet(f'background-color: {THEME_COLORS.INPUT_BACKGROUND_COLOR}; border-top-right-radius: {THEME_COLORS.INPUT_BORDER_RADIUS}px; border-bottom-right-radius: {THEME_COLORS.INPUT_BORDER_RADIUS}px; border-top-left-radius: 0; border-bottom-left-radius: 0; border: 0; border: {THEME_COLORS.INPUT_BORDER_WIDTH}px solid {THEME_COLORS.INPUT_BORDER_COLOR}; border-left: none;')
        self.go_button.clicked.connect(self._emit_change)
        layout.addWidget(self.go_button)
        layout.setStretchFactor(self.go_button, 0)


    def eventFilter(self, obj, event): # CHeck if enter was pressed
        if event.type() == QEvent.Type.KeyPress: # and obj is self.input_field 
            if event.key() == Qt.Key.Key_Return.value:
                self._emit_change()
            else:
                self.typing.emit(self.getValue())
        
        return super().eventFilter(obj, event)

    def set_focus(self):
        self.input_field.setFocus()

    # Internal call/connect
    def _emit_change(self):
        self.search.emit(self.getValue())

    def clearValue(self):
        self.input_field.setText('')

    def setValue(self, value: str = ''):
        self.input_field.setText(value)

    def getValue(self):
        return self.input_field.text()