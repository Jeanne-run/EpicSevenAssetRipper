from PyQt6.QtCore      import QCoreApplication, Qt
from PyQt6.QtWidgets   import QWidget, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui       import QFont

from app.constants     import VERSION
from .dialog_window    import ScrollableDialogWindow
from .button           import Button
from app.update        import download_update, update_check, unpack_update
from ..util.threads    import ThreadPool, Worker
from app.strings       import translate

import datetime

class UpdateDialog(ScrollableDialogWindow):
    download_link: str = None

    def __init__(self, parent=None):
        super().__init__(parent, title=translate('version_update_title'))

        self.check_for_updates()

        self.show()

    def check_for_updates(self):
        self.checking_for_updates_view()
        checker = Worker(update_check)
        checker.signals.result.connect(self.update_checker_done)
        ThreadPool.start(checker)

    def update_checker_done(self, args, result: list | None):
        if result is None:
            self.no_update_found_view()
        elif len(result) == 0:
            self.no_update_found_view()
        else:
            self.download_link = result[0]['zip_source']
            self.update_changelog_view(result)

    def download_and_apply_patch(self):
        download_update(self.download_link)
        unpack_update()

    def start_update_download(self):
        self.checking_for_updates_view()
        downloader = Worker(self.download_and_apply_patch)
        downloader.signals.result.connect(self.download_complete_view)
        downloader.signals.error.connect(self.download_error_view)
        ThreadPool.start(downloader)

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




    def clear_view(self):
        self.clear_header()
        self.clear_body()
        self.clear_footer()

    def checking_for_updates_view(self):
        self.clear_view()
        l = QLabel(self)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setText(translate('update_checking'))
        self.body.layout().addWidget(l)

    def no_update_found_view(self):
        self.clear_view()
        l = QLabel(self)
        l.setText(translate('current_is_latest_version'))
        self.body.layout().addWidget(l)
        self.body.layout().setAlignment(l, Qt.AlignmentFlag.AlignCenter)

        close_btn = QPushButton(self)
        close_btn = Button(self, translate('close'), pointer = True)
        close_btn.clicked.connect(self.close)
        self.footer.layout().addWidget(close_btn)

    def update_changelog_view(self, versions = []):
        self.clear_view()

        font_title = QFont()
        font_title.setPixelSize(18)
        font_title.setBold(True)

        l = QLabel(self)
        l.setText(translate('version_update_info').format(VERSION, versions[0]['version']))
        self.header.layout().addWidget(l)

        self.body.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setSpacing(10)

        for version in versions:
            l = QLabel(self)
            l.setText(f"⦿ {version['version']} - {datetime.datetime.fromisoformat(version['date']).strftime('%d %b %Y %H:%M')}")
            l.setFont(font_title)
            self.body.layout().addWidget(l)

            l = QLabel(self)
            l.setText(version['changelog'])
            l.setWordWrap(True)
            l.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            l.setContentsMargins(25,0,0,0)
            self.body.layout().addWidget(l)

        if self.download_link:
            update_btn = Button(self, translate('update_download'), pointer = True)
            update_btn.clicked.connect(self.start_update_download)
            self.footer.layout().addWidget(update_btn)

        close_btn = Button(self, translate('close'), pointer = True)
        close_btn.clicked.connect(self.close)
        self.footer.layout().addWidget(close_btn)

        self.setMinimumHeight(400)

    def downloading_update_view(self):
        self.clear_view()
        l = QLabel(self)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setText(translate('update_downloading_info'))
        self.body.layout().addWidget(l)

    def download_complete_view(self):
        self.clear_view()
        l = QLabel(self)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setText(translate('update_download_complete'))
        self.body.layout().addWidget(l)

        restart_btn = Button(self, translate('restart_now'), pointer = True)
        restart_btn.clicked.connect(self.restart_now)
        self.footer.layout().addWidget(restart_btn)

        close_btn = QPushButton(self)
        close_btn = Button(self, translate('restart_later'), pointer = True)
        close_btn.clicked.connect(self.close)
        self.footer.layout().addWidget(close_btn)

    def download_error_view(self):
        self.clear_view()
        l = QLabel(self)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setText(translate('update_download_error'))
        self.body.layout().addWidget(l)

        restart_btn = Button(self, translate('retry'), pointer = True)
        restart_btn.clicked.connect(self.start_update_download)
        self.footer.layout().addWidget(restart_btn)

        close_btn = QPushButton(self)
        close_btn = Button(self, translate('close'), pointer = True)
        close_btn.clicked.connect(self.close)
        self.footer.layout().addWidget(close_btn)