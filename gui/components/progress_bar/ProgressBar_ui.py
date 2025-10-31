from PyQt6.QtWidgets   import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QDialog, QPushButton, QLayout, QScrollArea
from PyQt6.QtCore      import Qt
from PyQt6.QtGui       import QIcon
from gui.util.svg_icon import QIcon_from_svg
from app.strings       import translate

_BAR_WIDGET_HEIGHT = 70

class Progress(QWidget):
    def __init__(self, parent, can_cancel=True):
        super().__init__(parent)

        self._parent = parent
        parent.layout().addWidget(self)

        self.setFixedHeight(_BAR_WIDGET_HEIGHT)
        self.setStyleSheet('margin: 0')
        wrapper = QVBoxLayout()
        wrapper_bar = QHBoxLayout()
        # error_wrap = QHBoxLayout()
        self.setLayout( wrapper )
        
        self.progress_info_label = QLabel()
        self.progress_info_label.move( 30, 10 )
        self.progress_info_label.adjustSize()
        self.progress_info_label.setText('')
        wrapper.addWidget( self.progress_info_label )

        wrapper.addLayout( wrapper_bar )

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressbar")
        self.progressBar.setVisible(True)
        wrapper_bar.addWidget(self.progressBar)

        if can_cancel:
            self.cancel_button = QPushButton()
            self.cancel_button.clicked.connect(self.remove)
            self.cancel_button.setIcon(QIcon(QIcon_from_svg('trash-can-outline', QApplication.instance().ThemeColors.BUTTON_CRITICAL_FONT_COLOR)))
            self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.cancel_button.setText(translate('cancel'))
            self.cancel_button.setProperty('class', 'critical-button')
            wrapper_bar.addWidget(self.cancel_button)

        # wrapper.addLayout(error_wrap)
        # error = QLabel()
        # error.adjustSize()
        # error.setText('Some error')
        # error.setProperty('class', 'error-text')
        # error_wrap.addWidget( error )
    
    def setValue(self, value):
        self.progressBar.setProperty("value", value)

    def setLabel(self, text):
        self.progress_info_label.setText(text)

    def remove(self):
        self._parent.remove( self )


class Ui_Form(object):
    _progress_bars: list[Progress] = []

    def setupUi(self: QDialog):

        # self.setLayout( QVBoxLayout() )
        # scrollWidget =  QScrollArea( )
        # scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # self.layout().addWidget(scrollWidget)
        # mainWidget = QWidget( scrollWidget )

        self.setFixedWidth(550)
        # self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        # self.setSizeGripEnabled(False)
        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self._layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # self.setLayout(self._layout)

        self.setLayout(self._layout)

        # self.new()

    def new(self: QDialog, value: int = 0, text = ''):
        bars = len(self._progress_bars) + 1
        if bars == 1:
            self.show()

        widget = Progress( self )

        widget.setValue(value)

        widget.setLabel(text)

        # self._layout.addWidget(widget)

        self._progress_bars.append( widget )

        # self.setFixedSize(550, self.minimumSizeHint().height())

        self.setFixedHeight( bars*_BAR_WIDGET_HEIGHT + 22 )

        return widget

    def remove(self: QDialog, bar: Progress):
        if bar in self._progress_bars:
            index = self._progress_bars.index( bar )
            widget = self._progress_bars.pop( index )
            self._layout.removeWidget( widget )

            widget.destroy(True, True)
            widget.deleteLater()

            bars = len(self._progress_bars)

            if bars == 0:
                app: QMainWindow = self.app.property('MainWindow')
                if app and not app.isHidden():
                    # When hiding a dialog the main window will also disappear (go in the background/under other programs)
                    # this will give the main window focus before hiding the dialog box
                    app.activateWindow()
                    self.hide()
                else: # No app window and all child progress bars removed -> remove this window
                    self.close()
            else:
                self.setFixedHeight( bars*_BAR_WIDGET_HEIGHT + 22 )
        
    def remove_all(self):
        for item in self._progress_bars.copy():
            item.remove()

    def activeBars(self):
        return self._progress_bars

    def getProgressBar(self: QDialog, index = 0):
        print('remove all call')
        if index > len(self._progress_bars) -1:
            index = len(self._progress_bars) -1
        
        return self._progress_bars[index]