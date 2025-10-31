from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore    import Qt

class Button(QPushButton):
    def __init__(self, parent: QWidget | None = None, text = '', pointer: bool = False, minimum_width: int = None, disabled = False):
        super().__init__(parent)
        self.setText(text)
        if pointer: self.setCursor(Qt.CursorShape.PointingHandCursor)
        if minimum_width: self.setMinimumWidth(minimum_width)
        self.setDisabled(disabled)