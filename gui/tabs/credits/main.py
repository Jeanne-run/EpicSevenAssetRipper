from PyQt6.QtWidgets              import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore                 import Qt
from PyQt6.QtGui                  import QPixmap
from app.constants                import VERSION
from app.strings                  import translate
from app.update                   import update_check
from gui.components.button        import Button
from gui.components.update_dialog import UpdateDialog

class CreateTab(QWidget):
    order = 99
    def __init__(self, parent: QWidget | QMainWindow):
        super().__init__(parent)
        self.name = translate('credits')
        vertical_box = QVBoxLayout()
        self.setLayout(vertical_box)
        vertical_box.addStretch()

        ## APP ICON
        app_icon = QLabel(self)
        pixmap = QPixmap('./gui/assets/icon.png')
        app_icon.setPixmap(pixmap)
        app_icon.setScaledContents(True)
        app_icon.setFixedSize(int(pixmap.width() * 200//pixmap.height()), 200)
        vertical_box.addWidget(app_icon)
        vertical_box.setAlignment(app_icon, Qt.AlignmentFlag.AlignCenter)

        ## APP NAME
        app_name = QLabel(self)
        app_name.setText(f'{translate("app_name")} v{VERSION}')
        app_name.setStyleSheet('font-size: 18px')
        vertical_box.addWidget(app_name)
        vertical_box.setAlignment(app_name, Qt.AlignmentFlag.AlignCenter)

        ## GITHUB LINK
        github = QLabel(self)
        github.setText(f'<a href="https://github.com/CeciliaBot" style="color: {QApplication.instance().ThemeColors.LINK_FONT_COLOR}">{translate("github_page")}</a>')
        github.setOpenExternalLinks(True)
        vertical_box.addWidget(github)
        vertical_box.setAlignment(github, Qt.AlignmentFlag.AlignCenter)

        ## ICONS
        picto = QLabel(self)
        picto.setText(f'Material Design icons by <a href="https://pictogrammers.com/" style="color: {QApplication.instance().ThemeColors.LINK_FONT_COLOR}">pictogrammers</a>')
        picto.setOpenExternalLinks(True)
        vertical_box.addWidget(picto)
        vertical_box.setAlignment(picto, Qt.AlignmentFlag.AlignCenter)

        ## UPDATE BUTTON
        check_for_updates = Button(self, text=translate('check_updates'), pointer=True)
        check_for_updates.clicked.connect(self.check_for_app_updates)
        vertical_box.addSpacing(20)
        vertical_box.addWidget(check_for_updates)
        vertical_box.setAlignment(check_for_updates, Qt.AlignmentFlag.AlignCenter)
        self.updates_btn = check_for_updates


        vertical_box.addStretch()

    def check_for_app_updates(self):
        self.updates_btn.setDisabled(True)
        self.updates_btn.setText(translate('please_wait'))

        updates = update_check()

        if updates and len(updates) > 0:
            dialog = UpdateDialog(self, updates)
            dialog.closeEvent = lambda *a: self.updates_btn.setDisabled(False)
            print('Update found!')

        self.updates_btn.setText(translate('check_updates'))


