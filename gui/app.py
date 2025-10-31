
import sys
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore    import Qt, QLocale
from PyQt6.QtGui     import QPixmap, QIcon
from app.strings     import translate, setLocale
from app             import settings
from .theme .theme   import use_theme

try: import ctypes
except ImportError: ctypes = None


def CreateApp():
    if os.name == 'nt' and ctypes:
        try:
            # Set app id for windows to separate this app from the default python script icon in the task bar
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'ceciliabot.epicseven.assetripper.2')
        except Exception:
            pass

    setLocale(settings.getLanguage(fallback=QLocale.languageToCode(QLocale.system().language())))

    app = QApplication(sys.argv)
    app.setApplicationName(translate('app_name'))
    app.setWindowIcon(QIcon("./gui/assets/icon.png")) # Set deafult icon to be used in all windows
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    # app.setStyle('fusion')

    splash_pix = QPixmap('./gui/assets/icon.png')
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.SplashScreen)
    splash.show()

    # splash.showMessage(splash.tr('check_updates'), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
    # from app.update import update_check
    # update = update_check()

    use_theme(app)
    
    from .window         import AppMainWindow
    MainWindow = AppMainWindow()
    MainWindow.PluginToolbar.load_hooks()
    MainWindow.show()

    setattr(MainWindow, 'tr', translate)

    # Remove splash screen once MainWindow is ready
    splash.finish(MainWindow)

    app.exec()

if __name__ == '__main__':
    CreateApp()