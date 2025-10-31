from app.constants     import VERSION
from .dialog_window    import ScrollableDialogWindow
from .progress_bar.ProgressBar_ui import Progress
from .progress_bar.ProgressBar import ProgressBar as ProgressBarDialog

from PyQt6.QtCore      import QCoreApplication
from PyQt6.QtWidgets   import QWidget, QLabel, QPushButton
from PyQt6.QtGui       import QFont
from app.update        import download_update


import datetime

class UpdateDialog(ScrollableDialogWindow):
    download_link: str = None

    def __init__(self, parent=None, versions = []):
        super().__init__(parent, window_title='Version Updater')

        self.setFixedSize(450, 500)
        
        font_title = QFont()
        font_title.setPixelSize(18)
        font_title.setBold(True)

        if len(versions) > 0:
            self.download_link = versions[0]['url'][0]

            l = QLabel(self)
            l.setText(f"Current Version {VERSION}\nLatest: {versions[0]['version']}")
            self.addWidget(l)

            for version in versions:
                l = QLabel(self)
                l.setText(f"{version['version']} - {datetime.datetime.fromisoformat(version['date']).strftime('%d %b %Y %H:%M')}")
                l.setFont(font_title)
                self.addWidget(l)

                l = QLabel(self)
                l.setText(version['changelog'])
                self.addWidget(l)
        else:
                l = QLabel(self)
                l.setText('You have the latest version available!')
                self.addWidget(l)

        if len(versions) > 0:
            close_btn = QPushButton(self)
            close_btn.setText('Download Update')
            close_btn.clicked.connect(self.start_update_download)
            self.addWidget(close_btn)

        close_btn = QPushButton(self)
        close_btn.setText('Close')
        close_btn.clicked.connect(self.close)
        self.addWidget(close_btn)

    def clear_view(self):
        for item in self.widget.children():
            if item == self.main_content_area: continue

            self.main_content_area.removeWidget(item)

    def restart_now(self):
        import os
        import sys
        app = QCoreApplication.instance()
        window: QWidget = app.property('MainWindow')
        window.close()
        window.deleteLater()
        self.close()
        app.quit()
        os.execv(sys.executable, ['python'] + sys.argv)

    def start_update_download(self):
        self.clear_view()

        bar = Progress(self.widget, can_cancel=False)
        bar.setValue(66)
        bar.setLabel('Downloading update')
        download_update(self.download_link)
        self.clear_view()
        self.download_complete_view()

    def download_complete_view(self):
        l = QLabel(self)
        l.setText('Download complete, the patch will be applied after restart!')
        self.addWidget(l)

        restart_btn = QPushButton(self)
        restart_btn.setText('Restart now')
        restart_btn.clicked.connect(self.restart_now)
        self.addWidget(restart_btn)

        close_btn = QPushButton(self)
        close_btn.setText('Close')
        close_btn.clicked.connect(self.close)
        self.addWidget(close_btn)