from PyQt6.QtWidgets    import QApplication, QWidget, QDialog, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtGui        import QPixmap, QMovie
from PyQt6.QtCore       import Qt, QByteArray, QBuffer

from typing             import Literal, Callable, Tuple

from app.strings        import translate
from app.constants      import IMG_FORMATS
from app.util.types     import FileType
from ..util.threads     import Worker, ThreadPool
from ..util.svg_icon    import QIcon_from_svg
from .spinner           import Spinner
from .csv_viewer.table  import CSVView

PreviewWidgetTypes = Literal['image', 'csv', 'json', 'text']
ContentGetterArgType = Callable[[], bytes | bytearray | str]

class FileContentPreview(QWidget):
    '''
    You can set the preview type of a file format by calling:
    FileContentPreview.setPreviewType(format: str, PreviewWidgetType: str)
    '''

    is_windowed = False
    previewedWidget: QPixmap | QLabel = None
    currentPreviewArgs: Tuple[FileType, bytes | bytearray | str] = ()
    worker: Worker = None

    '''
    For each format set a preview type
    '''
    fileFormatToPreview: dict[str, PreviewWidgetTypes] = {
        'json': 'json',
        'timeline': 'json',
        'tsv': 'csv',
        'csv': 'csv',
        'txt': 'text',
        'atlas': 'text',
        'bat': 'text',
        'py': 'text',
        'js': 'text'
    }

    def __init__(self, parent: QWidget | None = None, is_windowed=False):
        super().__init__(parent)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.layout().setContentsMargins(0,0,0,0)
        self.setProperty('class', 'file-preview')

        self.removeCurrentWidget()
        
        # Buttons
        self.header_widget = QWidget()
        self.header_widget.hide()
        hLine = QHBoxLayout()
        hLine.setContentsMargins(0,0,0,0)
        hLine.setSpacing(6)
        self.header_widget.setLayout(hLine)
        self.layout().addWidget(self.header_widget)

        self.label_title = QLabel(text=translate('preview'))
        hLine.addWidget(self.label_title)
        hLine.setStretchFactor(self.label_title, 0)
        self.label_title.setHidden(is_windowed)

        if not is_windowed:
            hLine.addStretch()

            close = QPushButton()
            close.setText('Windowed')
            close.setIcon(QIcon_from_svg('open-in-new', QApplication.instance().ThemeColors.BUTTON_FONT_COLOR))
            close.setToolTip('Open this preview in a separate window.')
            close.setCursor(Qt.CursorShape.PointingHandCursor)
            close.clicked.connect(self._open_windowed)
            hLine.addWidget(close)   

            close = QPushButton()
            close.setText('✕')
            close.setCursor(Qt.CursorShape.PointingHandCursor)
            close.setFixedWidth(25)
            close.clicked.connect(self.hide)
            hLine.addWidget(close)

        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.layout().addWidget(self.scrollWidget)

        self.create_spinner()

    def is_preview_supported(self, file_format: str) -> bool:

        if file_format in IMG_FORMATS or file_format in self.fileFormatToPreview:
            return True

        return False

    def create_spinner(self):
        self.spinner = Spinner()
        self.spinner_wrapper = QWidget()
        self.spinner_wrapper.setLayout(QVBoxLayout())
        self.spinner_wrapper.layout().addWidget(self.spinner)
        self.spinner_wrapper.layout().setAlignment(self.spinner, Qt.AlignmentFlag.AlignCenter)
        self.spinner_wrapper.setContentsMargins(0,0,0,0)
        self.layout().addWidget(self.spinner_wrapper)
        self.layout().setStretchFactor(self.spinner_wrapper, 1)
        self.spinner_wrapper.setHidden(True)
        return self.spinner
    
    def hide_spinner(self):
        self.spinner.stop()
        self.spinner_wrapper.setHidden(True)
        self.scrollWidget.setHidden(False)

    def show_spinner(self):
        self.spinner.start()
        self.spinner_wrapper.setHidden(False)
        self.scrollWidget.setHidden(True)
    
    def _create_window(self, title):
        window = QDialog(
            parent=self,
            flags=Qt.WindowType.Window |
                Qt.WindowType.WindowTitleHint |
                Qt.WindowType.WindowMaximizeButtonHint |
                Qt.WindowType.WindowCloseButtonHint |
                Qt.WindowType.WindowMinimizeButtonHint
        )
        window.setMinimumSize(200, 200)
        window.setBaseSize(200,200)
        window.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        window.setWindowTitle(title)
        window.setWindowRole('preview')
        window.setLayout(QHBoxLayout())
        window.layout().setContentsMargins(0,0,0,0)
        window.show()
        preview = FileContentPreview(is_windowed=True)
        window.layout().addWidget(preview)
        return window, preview

    def  _open_windowed(self):
        '''
            open the preview in a new window (internal usage)
        '''
        window, preview = self._create_window(self.currentPreviewArgs[0]['full_path'])
        # Passing the content directly to avoid another loading and pack reading
        preview._display(*self.currentPreviewArgs)

    def display_windowed(self, file: FileType, get):
        '''
            open the preview directly in a new window
        '''
        window, preview = self._create_window(file['full_path'])
        preview.display(file, get)

    @staticmethod
    def setPreviewType(format: str, preview_type: PreviewWidgetTypes):
        if not format or not preview_type:
            return
        FileContentPreview.fileFormatToPreview[format] = preview_type

    @staticmethod
    def deletePreviewType(format: str):
        if not format:
            return
        del FileContentPreview.fileFormatToPreview[format]

    @staticmethod
    def getFormatPreviewWidget(format):
        return FileContentPreview.fileFormatToPreview.get(format)

    def _imageWidget(self, content):
        wid = QLabel()
        image = QPixmap()
        image.loadFromData(content)
        wid.setPixmap(image)
        wid.setContentsMargins(0,0,0,0)
        wid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollWidget.setWidget(wid)
        self.previewedWidget = wid

    def _plainTextWidget(self, content: bytes | bytearray | str):
        if isinstance(content, bytes) or isinstance(content, bytearray):
            content = content.decode('utf-8')

        wid = QPlainTextEdit()
        wid.setPlainText(content)
        wid.setReadOnly(True)
        self.scrollWidget.setWidget(wid)
        self.previewedWidget = wid

    def _csvTableWidget(self, content: bytes | bytearray | str):
        if isinstance(content, bytes) or isinstance(content, bytearray):
            content = content.decode('utf-8')

        data = content

        if not isinstance(data, list): # CSV viiewer can only work with a list[list[str | number]]
            range = content.split('\n')
            data = []

            for row in range:
                if row != '': # Sometimes the last line is empty
                    data.append(row.split('\t'))
        
        wid = CSVView(data=data)
        self.scrollWidget.setWidget(wid)
        wid.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.previewedWidget = wid

    def _animatedWidget(self, content: bytes | bytearray):
        '''
        This seems to crash even when callign is valid
        
        :param self:
        :param content: The bytes of the file
        :type content: bytes | bytearray
        '''
        import io
        wid = QLabel(self)
        movie = QMovie(self)
        movie.setDevice(QBuffer(QByteArray(io.BytesIO(content).getvalue())))
        movie.setCacheMode(QMovie.CacheMode.CacheAll)
        movie.setFormat(QByteArray(b'webp'))

        wid.setMovie(movie)
        movie.jumpToFrame( movie.frameCount() - 1 )
        self.scrollWidget.setWidget(wid)
        self.previewedWidget = wid
        movie.start()

    def _unknownPreviewWidget(self):
        wid = QLabel()
        wid.setText(f'File preview is not available for this content.')
        self.scrollWidget.setWidget(wid)

    def _display(self, file: FileType, content: bytearray | bytes | str):

        self.removeCurrentWidget()

        self.currentPreviewArgs = (file, content)

        _file_format = file.get('format')
        _type: PreviewWidgetTypes | None = self.getFormatPreviewWidget(_file_format) or ('image' if _file_format in IMG_FORMATS else None)

        try:
            match _type:
                case 'image':
                    self._imageWidget(content)
                case 'csv':
                    self._csvTableWidget(content)
                case 'text' | 'json':
                    self._plainTextWidget(content)
                case 'animated':
                    self._animatedWidget(content)
                case _:
                    self._unknownPreviewWidget()

            self.label_title.setText(f'Preview {_type}: {file.get("full_path")}')
            self.header_widget.show()

        except Exception as e:
            wid = QLabel()
            wid.setWordWrap(True)
            wid.setText(f'Preview error: {e}')
            self.scrollWidget.setWidget(wid)

    def display(self, file: FileType, getter: ContentGetterArgType, windowed=False):
        '''
        Run the getter in a thread and pass it's result to self._display
        '''
        if windowed:
            return self.display_windowed(file, getter)

        self.header_widget.hide()

        if self.worker:
            self.worker.signals.finished.disconnect()
            self.worker.signals.result.disconnect()

        self.setHidden(False)

        self.show_spinner()

        # Get data in thread
        worker = Worker(getter)
        worker.signals.finished.connect( self.worker_finished )
        worker.signals.result.connect( lambda args, result: self._display( file, result ) )
        self.worker = worker
        ThreadPool.start(worker)

    def worker_finished(self, *args):
        self.hide_spinner()
        self.worker=None

    def removeCurrentWidget(self):
        self.currentPreviewArgs = []
        if self.previewedWidget:
            self.scrollWidget.setWidget(None)
            self.previewedWidget.deleteLater()
            self.previewedWidget = None

    def closeEvent(self, a0):
        if self.worker:
            self.worker.signals.finished.disconnect()
            self.worker.signals.result.disconnect()
            self.worker = None

        return super().closeEvent(a0)

    def hide(self):
        self.removeCurrentWidget()
        return super().hide()