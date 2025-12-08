import json
import re
from PyQt6.QtWidgets import QWidget, QTableView, QScrollArea, QCheckBox, QMenu, QVBoxLayout, QHBoxLayout, QToolBar, QStyle, QFileDialog
from PyQt6.QtCore    import Qt, QSize, QModelIndex
from PyQt6.QtGui     import QAction

from .model          import CsvTableModel, DelegateEditor
from ..search_bar    import SearchBar
from ..button        import Button

class CSVView(QWidget):
    data: list[list[str]] = []

    def __init__(self, parent = None, data = None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        #---- Toolbar
        self.toolbar = QToolBar("CSVToolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.layout().addWidget(self.toolbar)

        style_csv = self.toolbar.style()
        icon = style_csv.standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        self.button_csv = QAction(icon, "CSV", self)
        self.button_csv.setStatusTip("Export data to CSV file")
        self.button_csv.triggered.connect(self.onExportCSV)
        self.toolbar.addAction(self.button_csv)

        style_csv = self.toolbar.style()
        icon = style_csv.standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        self.button_csv = QAction(icon, "JSON", self)
        self.button_csv.setStatusTip("Export data to JSON file")
        self.button_csv.triggered.connect(self.onExportJSON)
        self.toolbar.addAction(self.button_csv)

        #---- CSV Table
        self.table = QTableView()
        self.table.setModel(CsvTableModel(data))
        self.table.setItemDelegate(DelegateEditor(self.table))
        self.setReadOnly(True)
        self.layout().addWidget(self.table)
        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()

        self.header = self.table.horizontalHeader()
        self.header.sectionClicked.connect(self.head_clicked)

        self.data = data

    def setReadOnly(self, value: bool):
        self.table.model()._setReadOnly(value)

    def onExportJSON(self):
        """ Export data to a JSON file """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Export CSV to JSON', '', ".json(*.json)")
        if file_name:
            result = []

            for i in range(1, len(self.data)):
                currentItem = self.data[i]
                itemData = {}

                for index, key in enumerate(self.data[0]):
                    if currentItem[index] != "":
                        itemData[key] = currentItem[index]

                result.append(itemData)

            with open(file_name, 'w') as f:
                f.write(json.dumps(result, indent=4))

    def onExportCSV(self):
        """ Export data to a CSV file, tab separator """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Export CSV to JSON', '', ".csv(*.csv)")
        if file_name:
            # self.data will be edited in the self.table.model so there is no need to read the table itself we can just use the data directly
            csv = '\n'.join([ '\t'.join(i) for i in self.data])

            with open(file_name, 'w') as f:
                f.write(csv)

    def head_clicked(self, index):
        model = self.table.model()
        head_menu = QMenu(self)
        head_menu_layout = QVBoxLayout()
        head_menu.setLayout(head_menu_layout)
        head_menu_layout.setSpacing(0)
        head_menu_layout.setContentsMargins(0,0,0,0)
        head_menu.setFixedWidth(200)
        head_menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        search = SearchBar(head_menu, placeholder=f'Search {self.table.model().headerData(index, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)}...')
        search.set_focus()
        head_menu.layout().addWidget(search)

        wrap_btn = QWidget(head_menu)
        wrap_btn.setLayout(QHBoxLayout())
        apply = Button(head_menu, text='Apply', pointer=True)
        cancel = Button(head_menu, text='Cancel', pointer=True)
        wrap_btn.layout().addWidget(apply)
        wrap_btn.layout().addWidget(cancel)
        head_menu.layout().addWidget(wrap_btn)

        def close():
            head_menu.close()
            head_menu.deleteLater()

        def filter_apply():
            _query = re.compile(search.getValue())
            for i in range(model.rowCount(0)):
                data = model.data(model.index(i, index), Qt.ItemDataRole.DisplayRole)
                self.table.setRowHidden(i, re.search(_query, data) is None)
            close()

        search.search.connect(filter_apply)

        cancel.clicked.connect(close)

        apply.clicked.connect(filter_apply)

        headerPos = self.mapToGlobal(self.header.pos())        
        posX = headerPos.x() + self.header.sectionViewportPosition(index) + self.header.sectionSize(index)//2-head_menu.width()//2
        posY = self.mapToGlobal(self.header.pos()).y() + self.header.height()
        head_menu.move(
            posX,
            posY
        )

        head_menu.show()