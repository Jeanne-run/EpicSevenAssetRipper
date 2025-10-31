from PyQt6.QtWidgets  import QApplication, QMainWindow, QDialog
from PyQt6.QtCore     import Qt, pyqtSlot
from PyQt6.QtGui      import QWindowStateChangeEvent
import sys

from .ProgressBar_ui import Ui_Form

default_flags = (Qt.WindowType.Window |
    Qt.WindowType.CustomizeWindowHint |
    Qt.WindowType.WindowTitleHint |
    # Qt.WindowType.WindowCloseButtonHint |
    Qt.WindowType.WindowMinimizeButtonHint)

class ProgressBar(QDialog, Ui_Form):
    '''
        Don't pass a parent if you want this window to have a separate icon in the OS taskbar
    '''

    def __init__(self, parent:QMainWindow=None, desc = None, app: QApplication = None, id: str = 'ProgressBarWindow', flags = default_flags ):
        super(ProgressBar, self).__init__(parent)
        self.setWindowFlags( flags )

        if not app:
            app = QApplication.instance()
        
        app.setProperty(id, self)
        self.app = app

        self.setupUi()

        # if parent:
        #     # parent.minimized.connect( self.showMinimized )
        #     # parent.restored.connect( self.showNormal )
        #     parent.destroyed.connect( self.remove_all )

        if desc != None:
            self.setDescription(desc)

    def promoteToWindow(self):
        '''
            Removes from the parents and adds minimize and close buttons
        '''
        save_geometry = self.geometry()
        self.setParent(None)
        self.overrideWindowFlags( Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint )
        if self.isHidden():
            self.setGeometry(save_geometry)
            self.setHidden(False)

    def setValue(self, val, index = 0): # Sets value
        self.getProgressBar(index).setValue(val)

    def setDescription(self, desc): # Sets Pbar window title
        self.setWindowTitle(desc)

    def setLabel(self, text, index = 0):
        self.getProgressBar(index).setLabel(text)

    def closeEvent(self, a0):
        self.remove_all()
        return super().closeEvent(a0)




def main():
    app = QApplication(sys.argv)      # A new instance of QApplication
    form = ProgressBar('')     # We set the form to be our MainWindow (design)
    bar1 = form.new()     # We set the form to be our MainWindow (design)
    bar1.setValue(40)
    bar1.setLabel('Copy')
    bar2 = form.new()
    bar2.setValue(70)
    bar2.setLabel('c:\\dsfsd')
    app.exec()                                 # and execute the app

if __name__ == '__main__':                      # if we're running file directly and not importing it
    main()                                      # run the main function
