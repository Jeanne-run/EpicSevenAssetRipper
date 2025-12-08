from PyQt6.QtWidgets        import QApplication, QMainWindow, QTabWidget, QWidget
from PyQt6.QtCore           import Qt, pyqtSignal
from app.constants          import VERSION
from .pugin_toolbar         import PuginToolbar
from app.strings            import translate
from app                    import settings
from .components.progress_bar.ProgressBar import ProgressBar
import os
import importlib
import glob


class AppMainWindow(QMainWindow):
    closed = pyqtSignal()
    PluginToolbar: PuginToolbar = None
    ProgressBarWindow: ProgressBar = None
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        app = QApplication.instance()
        app.setProperty('MainWindow', self)


        app.setProperty('GetProgressBarWindow', self.get_progress_bar_window)

        self.setWindowTitle(f'{translate("app_name")} v{VERSION}')
        self.resize(900, 700)

        self.PluginToolbar = PuginToolbar(self)

        self.tabs = QTabWidget()
        self.tabs.setEnabled(True)
        self.tabs.setObjectName("MainWindowTabs")
        self.tabs.setDocumentMode(True)

        self.setCentralWidget(self.tabs)
 
        # Get all folders containing a main.py script in the tabs folder and load them
        tabs: list[QWidget] = []
        py_files = glob.glob(os.path.join('gui', 'tabs', '*', 'main.py')) \
          + glob.glob(os.path.join('gui', 'tabs', '.*', 'main.py'))

        for py in py_files:
            path, file = os.path.split(py)
            _, ext = os.path.split(path)
            spec = importlib.util.spec_from_file_location(ext, os.path.join(path, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tabs.append(module.CreateTab(self))

        tabs.sort(reverse=False, key=lambda e: e.order)

        for tab in tabs:
            self.tabs.addTab(tab, tab.name)
    
    def get_progress_bar_window(self):
        if not self.ProgressBarWindow:
            self.ProgressBarWindow = ProgressBar(self, id='ProgressBarWindow', flags=Qt.WindowType.Window | Qt.WindowType.SubWindow )
        
        return self.ProgressBarWindow

    def closeEvent(self, a0):
        self.closed.emit()
        bars = self.get_progress_bar_window()
        if settings.getStopOnClose() == True: # Stop all threads
            bars.remove_all()
        else: # Make progress bar a standalone window
            if len( bars.activeBars() )>0:
                bars.promoteToWindow()

        return super().closeEvent(a0)