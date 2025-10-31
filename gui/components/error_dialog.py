from PyQt6.QtWidgets    import QMessageBox
from .button            import Button

def ErrorWindow(title, message, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    button = Button(text='Ok', pointer=True, minimum_width=150)
    msg.setDefaultButton(button)
    msg.setText(message)
    msg.setFixedWidth(550)
    # msg.setInformativeText('More information')
    msg.setWindowTitle(title)
    msg.exec()