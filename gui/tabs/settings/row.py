from PyQt6.QtWidgets        import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QFileDialog
from PyQt6.QtCore           import Qt
from PyQt6.QtGui            import QFont
from gui.components.switch  import AnimatedToggle
from gui.components.button  import Button

class SettingsRow(QWidget):
    def __init__(self, parent, title, description, type, value, onchanged, options=[]):
        super().__init__(parent)

        self.setObjectName('SettingRow')

        self.setProperty('class', 'setting-row')
        self.setStyleSheet(f'background-color: {QApplication.instance().ThemeColors.BUTTON_BACKGROUND_COLOR};')
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)


        text_wrapper = QWidget(self)
        layout.addWidget(text_wrapper)
        description_layout = QVBoxLayout()
        text_wrapper.setLayout(description_layout)

        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        title_label = QLabel(self)
        title_label.setText(title)
        title_label.setFont(title_font)
        description_layout.addWidget(title_label)

        description_label = QLabel(self)
        description_label.setText(description)
        description_label.setWordWrap(True)
        description_layout.addWidget(description_label)


        option_wrapper = QWidget(self)
        option_wrapper.setLayout(QVBoxLayout())
        option_widget = self.create_options_widget(type, value, onchanged, options)
        option_wrapper.layout().addWidget(option_widget)
        option_wrapper.layout().setAlignment(option_widget, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(option_wrapper)
        option_wrapper.setMaximumWidth(200)

        layout.setStretchFactor(option_wrapper, 0)

    def create_options_widget(self, sett_type, value, onchanged, options):
        match(sett_type):
            case 'checkbox':
                box = AnimatedToggle(self)
                box.setCheckState(Qt.CheckState.Checked if value == True else Qt.CheckState.Unchecked)
                box.stateChanged.connect(onchanged) # 2==checked 0 == unchecked
                return box
            case 'select':
                box = QComboBox(self)
                box.setMinimumWidth(100)
                box.addItems(options)
                box.setCurrentIndex(value)
                box.setCurrentText(options[value])
                box.currentIndexChanged.connect(onchanged)
                return box
            case 'path':
                box = Button(self, text=options, pointer=True, minimum_width=100)
                box.clicked.connect(lambda: onchanged(self._path_select(value)))
                return box

    def _path_select(self, value: str):
        return QFileDialog.getExistingDirectory(
            self,
            '',
            directory=value
        )