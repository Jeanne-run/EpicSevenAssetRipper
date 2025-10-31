from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore    import Qt
from gui.tabs.settings.row import SettingsRow
from gui.tabs.settings.default_options import OPTIONS

from app.strings import translate

class CreateTab(QWidget):
    order = 0
    def __init__(self, parent: QWidget | QApplication):
        super().__init__(parent)
        self.name = translate('settings')

        QApplication.instance().setProperty('CreateSetting', self.add_settings_row)


        self_layout = QHBoxLayout()
        self.setLayout(self_layout)
        scroll = QScrollArea()
        widgetWrapper = QWidget()
        scroll.setWidget(widgetWrapper)
        self.settings_rows_layout = QVBoxLayout()
        widgetWrapper.setLayout(self.settings_rows_layout)
        self_layout.addWidget(scroll) #, 0, Qt.AlignmentFlag.AlignHCenter) #, 1, Qt.AlignmentFlag.AlignHCenter)

        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(1000)
        # self_layout.setAlignment(scroll, Qt.AlignmentFlag.AlignCenter)

        for row in OPTIONS:
            self.add_settings_row(title=row[0], description=row[1], type=row[2], value=row[3], options=row[4], onchanged=row[5])



    def add_settings_row(self, title, description, type, value, onchanged=lambda *arg: 0, options=[]):
        widget = SettingsRow(self, title=title, description=description, type=type, value=value, onchanged=onchanged, options=options)

        self.settings_rows_layout.addWidget(widget)

        return widget
