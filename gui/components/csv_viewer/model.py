from PyQt6.QtCore    import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QItemDelegate

class CsvTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._setReadOnly()
        self._data = data

    def rowCount(self, index) -> int:
        # -1 because of the header being in the same array/list
        return len(self._data) - 1 if self._data else 0

    def columnCount(self, index) -> int:
        return len(self._data[0]) if self._data else 0
    
    def _setReadOnly(self, value: bool=True):
        self._flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable if value else Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def flags(self, index):
        return self._flags

    def headerData(self, section: int, orientation, role: int) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Vertical:
                return section + 1 # row names
            elif orientation == Qt.Orientation.Horizontal:
                return self._data[0][section] # column names
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft + Qt.AlignmentFlag.AlignVCenter

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                value = self._data[index.row() + 1][index.column()]
            except IndexError:
                value = ''

            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
        
    def _data_getter(self, row: int, column: int):
        return str(self._data[row + 1][column])
    

class DelegateEditor(QItemDelegate):
    def setEditorData(self, editor, index):
        text = index.data(Qt.ItemDataRole.EditRole) or index.data(Qt.ItemDataRole.DisplayRole)
        editor.setText(text)

    def setModelData(self, editor, model: CsvTableModel, index):
        model._data[index.row()+1][index.column()] = editor.text()