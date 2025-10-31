from PyQt6.QtWidgets        import QApplication, QToolBar, QMainWindow, QLabel, QSizePolicy
from PyQt6.QtCore           import Qt, QSize
from PyQt6.QtGui            import QAction
from .util.svg_icon         import QIcon_from_svg
from app.load_hooks         import HookClass, load_hooks
from app.strings            import translate

class PuginToolbar(QToolBar):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setObjectName('PluginToolbar')
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setMovable(False)
        self.setIconSize(QSize(16, 16))
        self.setMinimumHeight(27)
        self.setAutoFillBackground(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        parent.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self)

        reload_action = QAction(translate('reload_plugin_tooltip'), parent)
        reload_action.setStatusTip(translate('reload_plugin_tooltip'))
        reload_action.setIcon(QIcon_from_svg('refresh.svg', QApplication.instance().ThemeColors.TOOLBAR_ICON_COLOR))
        reload_action.setObjectName('RELOAD_HOOKS_ACTION')
        reload_action.triggered.connect(self.refresh_plugins)
        self.addAction(reload_action)
        self.widgetForAction(reload_action).setCursor(Qt.CursorShape.PointingHandCursor)

        bottom_description = QLabel()
        bottom_description.setText('')
        bottom_description.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bottom_description.setEnabled(True)
        bottom_description.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bottom_description.setObjectName('BOTTOM_INFO_TEXT')
        self.addWidget(bottom_description)
        self.info_label = bottom_description

        self.setProperty('class', 'BottomToolbar')

    def setText(self, value):
        self.info_label.setText(value)

    def create_add_on_buttons(self, plugin: HookClass):
        q = QAction(plugin.get_name(), self)
        q.setObjectName('ADDON_ICON')
        q.setCheckable(True)
        q.setChecked(plugin.get_is_enabled())
        q.toggled.connect(plugin.set_is_enabled)
        self.addAction(q)
        self.widgetForAction(q).setCursor(Qt.CursorShape.PointingHandCursor)

    def load_hooks(self):
        return load_hooks(gui_create=self.create_add_on_buttons)

    def refresh_plugins(self):
        self.setText(translate('reloading_plugin'))

        children = self.findChildren(QAction, 'ADDON_ICON')
        for child in children:
            self.removeAction(child)
        children = None
        
        loaded, errors = self.load_hooks()

        self.setText(translate('reload_plugin_done').format(loaded, errors))