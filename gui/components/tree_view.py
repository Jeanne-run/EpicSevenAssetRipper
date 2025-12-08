import os
import re
from typing             import List
from PyQt6.QtWidgets    import QApplication, QTreeWidget, QTreeWidgetItem, QMenu
from PyQt6.QtCore       import Qt, QUrl, QMimeData, QVariant, pyqtSignal, QObject
from PyQt6.QtGui        import QAction, QIcon, QColor, QDrag

from app.util.tree      import create_folder
from app.util.types     import FileTreeType, FileType, FolderType
from ..util.svg_icon    import QIcon_from_svg
from ..util.mouse       import mouse_pressed
from app.util.file      import convert_size
from app.constants      import IMG_FORMATS, TEMP_FOLDER


class DelayedMimeData(QMimeData):

    def __init__(self):
        super().__init__()
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def retrieveData(self, mime_type: str, preferred_type: QVariant):
        if not mouse_pressed():
            for callback in self.callbacks.copy():
                self.callbacks.remove(callback)
                callback()

        p = QMimeData.retrieveData(self, mime_type, preferred_type)
        return p


    def eventFilter(self, *args):
        print(args)







class CustomQTreeWidgetItem(QTreeWidgetItem):
    _query_pass: bool = True # Item is not hidden by search query
    _compare_pass: bool = True # Item is not hidden by compare
    ____data: FileType | FolderType = {}

    def __init__(self, parent = None):
        return super().__init__(parent)

    def getJSONData(self):
        return self.____data
    
    def setJSONData(self, data):
        # self.setData(0, 256, data) using set data causes a lot of memory usage
        self.____data = data

    def shouldShowItem(self):
        return self._query_pass and self._compare_pass





class TreeViewTable(QObject):
    treeItems = []
    treeData = []
    compareData = None
    tempDeletedNodes: List[CustomQTreeWidgetItem] = []
    contextMenuOptions = []
    # functionColumnContentItem = None

    dargdrop = pyqtSignal(list, str)

    def __init__(self):
        super().__init__()

        self.folderIcon = QIcon_from_svg('folder-outline', QApplication.instance().ThemeColors.FONT_COLOR)
        # self.fileIcon = QIcon( QIcon_from_svg('file.svg', QApplication.instance().ThemeColors.FONT_COLOR) )
        self.tree = QTreeWidget()
        self.tree.setColumnWidth(0,500)
        self.tree.setColumnWidth(1,70)
        self.tree.setColumnWidth(2,70)
        self.tree.setColumnWidth(3,100)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.setSelectionMode(self.tree.SelectionMode.ExtendedSelection)
        self.tree.setRootIsDecorated(True)
        self.tree.setSelectionBehavior(self.tree.SelectionBehavior.SelectRows)
        self.tree.setAlternatingRowColors(True)


        if mouse_pressed != None:
            self.tree.setDragEnabled( True )
            self.tree.setDragDropMode(self.tree.DragDropMode.DragOnly)
            self.tree.startDrag = self.startDrag

    def return_selected_items(self) -> List[CustomQTreeWidgetItem]:
        '''
            Return each element only once:
            If a parent folder and a child element are selected only the parent will be returned
        '''
        def any_parent_selected(item: CustomQTreeWidgetItem):
            parent = item.parent()
            while parent:
                if parent.isSelected():
                    return True
                else:
                    parent = parent.parent()
            return False
        
        return [ item for item in self.tree.selectedItems() if not any_parent_selected(item) ]

    def startDrag(self, actions):
        drag = QDrag(self.tree)
        data = self.fileTreeJsonFromSelection()
        mime = DelayedMimeData()
        path_list = []
        
        os.makedirs( TEMP_FOLDER, exist_ok=True )

        # mime.add_callback(lambda: self.write_temp_files(data, TEMP_FOLDER))
        mime.add_callback(lambda: self.dargdrop.emit(data, TEMP_FOLDER))

        for item in data:
            path = os.path.join(TEMP_FOLDER, item.get('name'))

            path_list.append(QUrl.fromLocalFile(path))

        mime.setUrls(path_list)
        mime.setData('application/x-qabstractitemmodeldatalist', b'') # self.tree.mimeData(self.tree.selectedItems()).data('application/x-qabstractitemmodeldatalist'))
        drag.setMimeData(mime)

        drag.exec(Qt.DropAction.MoveAction)







    def widget(self):
        return self.tree

    def clearTree(self):
        self.tree.selectionModel().clearSelection()
        self.tree.clear()
        self.compareData = None
        self.tempDeletedNodes = []
        # self.treeItems = []

    def showTree(self, tree_map):
        self.clearTree()
        self.addItems(self.tree, tree_map)
        self.treeData = tree_map

    def setColumns(self, columns):
        self.tree.setColumnCount(len(columns))
        self.tree.setHeaderLabels(columns)

    @staticmethod
    def __functionColumnContentItem(data):
        pass

    def setDictToColumn(self, fun):
        self.__functionColumnContentItem = fun

    def getTreeItemData(self, item: QTreeWidgetItem):
        return item.data(0 , 256)

    def getCurrentTreeData(self):
        return self.treeData

    def setWidgetItemText(self, item: CustomQTreeWidgetItem, data: FileTreeType):
        row = self.__functionColumnContentItem(data)
        for index, key in enumerate(row):
            if key is None:
                continue

            item.setText(index, key)

    def addItems(self, parent, items, callback=lambda _: 0):
        if not items:
            return None

        items.sort(key=self.sortByType, reverse=True)

        for item in items:
            try:
                treeitem = CustomQTreeWidgetItem(parent)
                treeitem.setJSONData(item)

                self.setWidgetItemText(treeitem, item)
                
                if item["type"] == "folder":
                    treeitem.setIcon(0, self.folderIcon )
                    self.addItems(treeitem, item["children"], callback=callback)

                callback(treeitem)

            except Exception as e:
                print(e)


    @staticmethod
    def sortByType(item):
        return item["type"]

#-------------------------------------- Search Filter Query ---------------------------------------------#
    def setQuery(self, query):
        try:
            self._query = re.compile(query)
        except:
            self._query = None
            return
        
        for i in range(self.tree.topLevelItemCount()):
            self._filterQuery(self.tree.topLevelItem(i))

    def _filterQuery(self, item: CustomQTreeWidgetItem) -> tuple[int, int]:
        if item._query_pass and not item.shouldShowItem(): # No need to check if the element is hidden by something else other than the query
            return 0, 0

        childCount = item.childCount()
        if childCount > 0:
            size = 0
            files = 0
            for i in range(childCount):
                child = item.child(i)
                c, s = self._filterQuery( child )
                files += c
                size += s

            item.setHidden(size == 0)

            if size > 0:
                item.setData(2, 0, convert_size(size))
                item.setData(3, 0, str(files) + ' files')

            return files, size

        else:
            if re.search(self._query, item.data(0, 0)):
                item._query_pass = True
                if item.shouldShowItem():
                    item.setHidden(False)
                    return 1, item.getJSONData()['size']
                else:
                    return 0, 0
            else:
                item._query_pass = False
                item.setHidden(not item.shouldShowItem())
                return 0, 0
            

#-------------------------------------- Compare ---------------------------------------------#
    def isComparing(self):
        return self.compareData != None
    
    def stopComparing(self):
        self.compareData = None
        ThemeColors = QApplication.instance().ThemeColors

        for item in self.tempDeletedNodes:
            parent = item.parent()
            if parent:
                parent.removeChild(item)

        def recursive(item: CustomQTreeWidgetItem, ThemeColors):
            childCount = item.childCount()
            if item._compare_pass: # if item was visible then it probably had a different color text
                item.setForeground( 0,  QColor(ThemeColors.FONT_COLOR) ) # Reset the font color for any item
            if childCount > 0:
                size = 0
                files = 0
                item._compare_pass = True
                for i in range(childCount):
                    c, s = recursive( item.child(i), ThemeColors )
                    files+=c
                    size += s

                item.setHidden(size == 0)

                if size > 0:
                    item.setData(2, 0, convert_size(size))
                    item.setData(3, 0, str(files) + ' files')

                return files, size

            else:
                item._compare_pass = True
                state = item.shouldShowItem()
                item.setHidden( not state )
                if state:
                    return 1, item.getJSONData()['size']
                else:
                    return 0, 0

        for i in range(self.tree.topLevelItemCount()):
            f,s = recursive(self.tree.topLevelItem(i), ThemeColors)

    def setCompare(self, compareTree):
        self.compareData = compareTree
        ThemeColors = QApplication.instance().ThemeColors

        def styleDeletedItem(item: CustomQTreeWidgetItem):
            if item not in self.tempDeletedNodes:
                self.tempDeletedNodes.append(item)

            c = item.childCount()

            for i in range(c):
                styleDeletedItem(item.child(i))

            item.setForeground(0, QColor(ThemeColors.TABLE_FONT_COLOR_FILE_DELETED))


        def recursive(treeItems: List[CustomQTreeWidgetItem], compData: FileTreeType, parent:CustomQTreeWidgetItem = None):
            nonlocal ThemeColors
            total_files = 0
            total_size  = 0

            for item in treeItems:
                data = item.getJSONData()
                d = None

                for compdata in compData:
                    if compdata['name'] == data['name'] and compdata['type'] == data['type']:
                        d = compdata
                        break

                if d is None: # New file
                    item._compare_pass = True
                    item.setForeground(0, QColor(ThemeColors.TABLE_FONT_COLOR_FILE_NEW))
                    if data['type'] == 'folder':
                        size = [item.child(i).getJSONData()['size'] for i in range(item.childCount()) if not item.child(i).isHidden()]
                        if len(size) > 0:
                            total_files += len(data['children'])
                            total_size += data['size']
                    elif item.shouldShowItem():
                        total_files += 1
                        total_size += data['size']

                else: # Old file
                    compData.pop( compData.index(d) )
                    if d['type'] == 'folder':
                        item._compare_pass = True
                        fi, si = recursive(
                            [item.child(i) for i in range(item.childCount())],
                            d['children'],
                            item
                        )
                        if fi > 0:
                            # No need to update the size and file count if it's hidden
                            item.setData(2, 0, convert_size(si))
                            item.setData(3, 0, str(fi) + ' files')
                            total_files += fi
                            total_size += si
                        item.setHidden( fi==0 )
                    else:
                        if d['size'] != data['size']:
                            item._compare_pass = True
                            item.setForeground(0, QColor(ThemeColors.TABLE_FONT_COLOR_FILE_EDITED))
                            if item.shouldShowItem():
                                total_size += data['size']
                                total_files += 1
                        else:
                            item._compare_pass = False
                            item.setForeground(0, QColor(ThemeColors.FONT_COLOR))

                        item.setHidden(not item.shouldShowItem())

            try:
                self.addItems(parent, compData, callback=styleDeletedItem)
                # Add the missing files as deleted
                # added = self.addItems(parent, compData, callback=styleDeletedItem)

                # self.tempDeletedNodes += added

                # for i in added:
                #     i.setForeground(0, QColor(ThemeColors.TABLE_FONT_COLOR_FILE_DELETED))

            except:
                pass
            
            return total_files, total_size
                        


        recursive(
            [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount())],
            compareTree,
            None
        )

    def fileTreeJsonFromSelection(self):
        '''
            Generate file view from the file tree selection without including hidden files
        '''
        return self.fileTreeJsonFromTreeItems( self.return_selected_items() )

    def fileTreeJsonFromView(self):
        '''
            Generate file view from the file tree without including hidden files
        '''
        return self.fileTreeJsonFromTreeItems( [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount()) ] )
    
    def fileTreeJsonImagesOnly(self):
        return 

    def fileTreeJsonFromTreeItems(self, items: List[CustomQTreeWidgetItem]):

        def recursive(item: CustomQTreeWidgetItem):
            i = item.childCount()
            if i > 0:
                data = item.getJSONData()
                content = [ recursive(item.child(j)) for j in range(i) if not item.child(j).isHidden() and item.child(j) not in self.tempDeletedNodes ]
                f = 0
                s = 0
                for x in content:
                    if x['type'] == 'folder':
                        f += x['files']
                    else:
                        f += 1
                    s += x['size']
                return create_folder(name=data['name'], files=f, size=s, children=content)
            else:
                return item.getJSONData()
        
        res = [ recursive(item) for item in items if not item.isHidden() and item not in self.tempDeletedNodes]

        return res
    

    def fileTreeJsonFromTreeItemsWithFormatFilter(self, formats: list[str] = IMG_FORMATS) -> FileTreeType:
        '''
            Generate a file tree from the current tree view containing only images
        '''

        def recursive(item: CustomQTreeWidgetItem):
            if item in self.tempDeletedNodes:
                return None
            
            i = item.childCount()
            if i > 0:
                data = item.getJSONData()
                content = [ recursive(item.child(j)) for j in range(i) if not item.child(j).isHidden() ]
                content = [c for c in content if c is not None]
                f = 0
                s = 0
                for x in content:
                    if x['type'] == 'folder':
                        f += x['files']
                    else:
                        f += 1
                    s += x['size']
                if f > 0:
                    return create_folder(name=data['name'], files=f, size=s, children=content)
                else:
                    return None
            else:
                data = item.getJSONData()
                if data['format'] in formats:
                    return data
                else:
                    return None
            
        res = [recursive(self.tree.topLevelItem(i)) for i in range(self.tree.topLevelItemCount())]
        res = [c for c in res if c is not None]

        return res