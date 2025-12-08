class LightTheme:
    BACKGROUND_COLOR = '#f0f0f0'
    FONT_COLOR = '#000000'
    LINK_FONT_COLOR = '#90c8f6'
    ICON_COLOR = FONT_COLOR
    BORDER_LIGHT_COLOR = '#d9d9d9'
    BORDER_HEAVY_COLOR = '#a0a0a0'
    INACTIVE_BACKGROUND_COLOR = '#f0f0f0'

    TOOLBAR_BACKGROUND_COLOR = '#f0f0f0'
    TOOLBAR_FONT_COLOR = FONT_COLOR
    TOOLBAR_ICON_COLOR = ICON_COLOR
    TOOLBAR_RADIUS = 0

    HOVER_BACKGROUND = '#d8eaf9'
    # HOVER_BORDER_WIDTH = 0
    # HOVER_BORDER_COLOR = HOVER_BACKGROUND
    HOVER_FONT_COLOR = FONT_COLOR
    
    SELECTION_BG_COLOR = '#c0dcf3'
    SELECTION_BORDER_WIDTH = 2
    SELECTION_BORDER_COLOR = '#90c8f6'
    SELECTION_FONT_COLOR = FONT_COLOR

    BUTTON_BACKGROUND_COLOR = '#e1e1e1'
    BUTTON_FONT_COLOR = FONT_COLOR
    BUTTON_BORDER_COLOR = '#adadad'
    BUTTON_BORDER_WIDTH = 1
    BUTTON_RADIUS = 0
    BUTTON_HOVER_BACKGROUND = '#e5f1fb'
    BUTTON_HOVER_BORDER_COLOR = '#007ad7'
    BUTTON_HOVER_FONT_COLOR = BUTTON_FONT_COLOR
    BUTTON_HOVER_BORDER_WIDTH = 2
    BUTTON_DISABLED_BACKGROUND_COLOR = '#cccccc'
    BUTTON_DISABLED_FONT_COLOR = '#787878'
    BUTTON_DISABLED_BORDER_COLOR = '#bfbfbf'
    BUTTON_DISABLED_BORDER_WIDTH = BUTTON_BORDER_WIDTH
    BUTTON_CRITICAL_BACKGROUND = BUTTON_BACKGROUND_COLOR
    BUTTON_CRITICAL_FONT_COLOR = 'red'
    BUTTON_CRITICAL_BORDER_COLOR = BUTTON_CRITICAL_FONT_COLOR
    BUTTON_CRITICAL_HOVER_BACKGROUND = HOVER_BACKGROUND
    BUTTON_CRITICAL_HOVER_FONT_COLOR = BUTTON_CRITICAL_FONT_COLOR
    BUTTON_CRITICAL_HOVER_BORDER_COLOR = BUTTON_CRITICAL_FONT_COLOR


    TAB_BACKGROUND_COLOR = BACKGROUND_COLOR
    TAB_BORDER_COLOR = BORDER_LIGHT_COLOR
    TAB_BORDER_BOTTOM_COLOR = 'transparent'
    TAB_BORDER_WIDTH = 1
    TAB_BORDER_RADIUS = 0
    TAB_MIN_WIDTH = 0
    TAB_ACTIVE_BACKGROUND_COLOR = '#ffffff'
    TAB_ACTIVE_FONT_COLOR = FONT_COLOR
    TAB_ACTIVE_BORDER_BOTTOM = SELECTION_BORDER_COLOR


    TABLE_HEAD_BACKGROUND_COLOR = '#ffffff'
    TABLE_HEAD_BORDER_COLOR = TABLE_HEAD_BACKGROUND_COLOR
    TABLE_ROW_FONT_COLOR = FONT_COLOR
    TABLE_ROW_ALTERNATE_BACKGROUND = '#ffffff'
    TABLE_FONT_COLOR_FILE_EDITED = 'orange'
    TABLE_FONT_COLOR_FILE_NEW = 'green'
    TABLE_FONT_COLOR_FILE_DELETED = 'red'

    INPUT_BACKGROUND_COLOR = '#ffffff'
    INPUT_FONT_COLOR = '#000000'
    INPUT_ICON_COLOR = INPUT_FONT_COLOR
    INPUT_BORDER_COLOR = BORDER_LIGHT_COLOR
    INPUT_BORDER_WIDTH = 1
    INPUT_BORDER_RADIUS = 6
    INPUT_DISABLED_FONT_COLOR = 'gray'

    PROGRESS_BAR_BACKGROUND = 'transparent'
    PROGRESS_BAR_RADIUS = 0
    PROGRESS_BAR_BORDER_COLOR = BORDER_LIGHT_COLOR

    SCROLLBAR_BACKGROUND = '#f0edf1'
    SCROLLBAR_HANDLE = '#888588'
    SCROLLBAR_WIDTH = 15
    SCROLLBAR_HANDLE_W = round(SCROLLBAR_WIDTH*0.3)
    SCROLLBAR_WIDTH = 15
    SCROLLBAR_HANDLE_W = round(SCROLLBAR_WIDTH*0.3)


class DarkTheme(LightTheme):
    BACKGROUND_COLOR = '#1f1f1f'
    FONT_COLOR = '#ffffff'
    LINK_FONT_COLOR = '#90c8f6'
    ICON_COLOR = FONT_COLOR
    BORDER_LIGHT_COLOR = '#414141'
    BORDER_HEAVY_COLOR = '#636363'
    INACTIVE_BACKGROUND_COLOR = '#000000'

    TOOLBAR_BACKGROUND_COLOR = '#333333'
    TOOLBAR_FONT_COLOR = FONT_COLOR
    TOOLBAR_ICON_COLOR = ICON_COLOR
    TOOLBAR_RADIUS = 0

    HOVER_BACKGROUND = "#4d4d4d"
    # HOVER_BORDER_WIDTH = 0
    # HOVER_BORDER_COLOR = HOVER_BACKGROUND
    HOVER_FONT_COLOR = FONT_COLOR
    
    SELECTION_BG_COLOR = '#777777'
    SELECTION_BORDER_WIDTH = 2
    SELECTION_BORDER_COLOR = '#3c3c3c'
    SELECTION_FONT_COLOR = FONT_COLOR

    BUTTON_BACKGROUND_COLOR = '#333333'
    BUTTON_FONT_COLOR = FONT_COLOR
    BUTTON_BORDER_COLOR = BUTTON_BACKGROUND_COLOR
    BUTTON_BORDER_WIDTH = 1
    BUTTON_RADIUS = 0
    BUTTON_HOVER_BACKGROUND = '#323232'
    BUTTON_HOVER_BORDER_COLOR = '#5d5d5d'
    BUTTON_HOVER_FONT_COLOR = BUTTON_FONT_COLOR
    BUTTON_HOVER_BORDER_WIDTH = 2
    BUTTON_DISABLED_BACKGROUND_COLOR = '#323130'
    BUTTON_DISABLED_FONT_COLOR = '#6a696b'
    BUTTON_DISABLED_BORDER_COLOR = BUTTON_DISABLED_BACKGROUND_COLOR
    BUTTON_DISABLED_BORDER_WIDTH = BUTTON_BORDER_WIDTH
    BUTTON_CRITICAL_BACKGROUND = BUTTON_BACKGROUND_COLOR
    BUTTON_CRITICAL_FONT_COLOR = 'red'
    BUTTON_CRITICAL_BORDER_COLOR = BUTTON_CRITICAL_FONT_COLOR
    BUTTON_CRITICAL_HOVER_BACKGROUND = HOVER_BACKGROUND
    BUTTON_CRITICAL_HOVER_FONT_COLOR = BUTTON_CRITICAL_FONT_COLOR
    BUTTON_CRITICAL_HOVER_BORDER_COLOR = BUTTON_CRITICAL_FONT_COLOR

    TAB_BACKGROUND_COLOR = INACTIVE_BACKGROUND_COLOR
    TAB_BORDER_COLOR = BORDER_LIGHT_COLOR
    TAB_BORDER_WIDTH = 1
    TAB_BORDER_RADIUS = 0
    TAB_MIN_WIDTH = 0
    TAB_ACTIVE_BACKGROUND_COLOR = BACKGROUND_COLOR
    TAB_ACTIVE_FONT_COLOR = FONT_COLOR
    TAB_ACTIVE_BORDER_BOTTOM = 'transparent'


    TABLE_HEAD_BACKGROUND_COLOR = BORDER_HEAVY_COLOR
    TABLE_HEAD_BORDER_COLOR = TABLE_HEAD_BACKGROUND_COLOR
    TABLE_ROW_FONT_COLOR = FONT_COLOR
    TABLE_ROW_ALTERNATE_BACKGROUND = '#2b2b2d'
    TABLE_FONT_COLOR_FILE_EDITED = 'yellow'
    TABLE_FONT_COLOR_FILE_NEW = 'green'
    TABLE_FONT_COLOR_FILE_DELETED = 'red'

    INPUT_BACKGROUND_COLOR = '#3f4042'
    INPUT_FONT_COLOR = FONT_COLOR
    INPUT_ICON_COLOR = INPUT_FONT_COLOR
    INPUT_BORDER_COLOR = BORDER_LIGHT_COLOR
    INPUT_BORDER_WIDTH = 1
    INPUT_BORDER_RADIUS = 0

    PROGRESS_BAR_BACKGROUND = 'transparent'
    PROGRESS_BAR_RADIUS = 0
    PROGRESS_BAR_BORDER_COLOR = BORDER_LIGHT_COLOR

    SCROLLBAR_BACKGROUND = '#171717'
    SCROLLBAR_HANDLE = '#4d4d4d'
    SCROLLBAR_WIDTH = 15
    SCROLLBAR_HANDLE_W = round(SCROLLBAR_WIDTH*0.3)
    SCROLLBAR_WIDTH = 15
    SCROLLBAR_HANDLE_W = round(SCROLLBAR_WIDTH*0.3)

class RoundedThemeParams:
    _BORDER_RADIUS = 4
    _BORDER_RADIUS_L = 6

    BUTTON_RADIUS = _BORDER_RADIUS
    TOOLBAR_RADIUS = _BORDER_RADIUS_L

    INPUT_BORDER_RADIUS = _BORDER_RADIUS_L
    PROGRESS_BAR_RADIUS = _BORDER_RADIUS_L
    TAB_BORDER_RADIUS = _BORDER_RADIUS_L

class RoundedDarkTheme(RoundedThemeParams, DarkTheme):
    TAB_BORDER_RADIUS = 0

class RoundedLightTheme(RoundedThemeParams, LightTheme):
    BUTTON_BORDER_WIDTH = 0
    BUTTON_HOVER_BORDER_WIDTH = 0
    BUTTON_DISABLED_BORDER_WIDTH = 0


class AccentColorDarkTheme(RoundedDarkTheme):
    _ACCENT = '#90CAF9'
    BUTTON_FONT_COLOR = _ACCENT
    BUTTON_BACKGROUNDG_COLOR = 'transparent'
    BUTTON_BORDER_COLOR = _ACCENT
    BUTTON_HOVER_BACKGROUND = _ACCENT
    BUTTON_HOVER_FONT_COLOR = '#ffffff'
    BUTTON_HOVER_BORDER_COLOR = _ACCENT

def apply(theme: LightTheme = AccentColorDarkTheme):
    return f"""
        QWidget {{
            color: {theme.FONT_COLOR};
            border: none;
            background-color: {theme.BACKGROUND_COLOR};
        }}

        QToolTip {{
            color: {theme.FONT_COLOR};
            border: none;
            background-color: {theme.BACKGROUND_COLOR};
        }}

        QGroupBox {{
            background-color: transparent;
            border: {theme.INPUT_BORDER_WIDTH}px solid {theme.BORDER_LIGHT_COLOR};
            border-radius: {theme.BUTTON_RADIUS}px;
            margin: 0.55em 0 0 0;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
        }}

        QMenu {{
            background-color: {theme.BACKGROUND_COLOR};
            border: {theme.BUTTON_BORDER_WIDTH}px solid {theme.BUTTON_BORDER_COLOR};
            color: {theme.BUTTON_FONT_COLOR};
        }}

        QMenu::item {{
            background-color: transparent;
        }}

        QMenu::item:selected {{
            background-color: {theme.HOVER_BACKGROUND};
            color: {theme.HOVER_FONT_COLOR};
        }}

        QPushButton {{
            background-color: {theme.BUTTON_BACKGROUND_COLOR};
            border: {theme.BUTTON_BORDER_WIDTH}px solid {theme.BUTTON_BORDER_COLOR};
            color: {theme.BUTTON_FONT_COLOR};
            border-radius: {theme.BUTTON_RADIUS}px;
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: {theme.BUTTON_HOVER_BACKGROUND};
            color: {theme.BUTTON_HOVER_FONT_COLOR};
            border: {theme.BUTTON_HOVER_BORDER_WIDTH}px solid {theme.BUTTON_HOVER_BORDER_COLOR};
        }}

        .critical-button {{
            background-color: {theme.BUTTON_CRITICAL_BACKGROUND};
            border: {theme.BUTTON_BORDER_WIDTH}px solid {theme.BUTTON_CRITICAL_BORDER_COLOR};
            color: {theme.BUTTON_CRITICAL_FONT_COLOR};
        }}
        .critical-button:hover {{
            background-color: {theme.BUTTON_CRITICAL_HOVER_BACKGROUND};
            border: {theme.BUTTON_HOVER_BORDER_WIDTH}px solid {theme.BUTTON_CRITICAL_HOVER_BORDER_COLOR};
            color: {theme.BUTTON_CRITICAL_HOVER_FONT_COLOR};
        }}

        QPushButton:disabled {{
            background-color: {theme.BUTTON_DISABLED_BACKGROUND_COLOR};
            color: {theme.BUTTON_DISABLED_FONT_COLOR};
            border: {theme.BUTTON_DISABLED_BORDER_WIDTH}pxpx solid {theme.BUTTON_DISABLED_BORDER_COLOR};
        }}
        


        QCheckBox {{
            color: {theme.FONT_COLOR};
        }}
        QLineEdit {{
            background-color: {theme.INPUT_BACKGROUND_COLOR};
            border: {theme.INPUT_BORDER_WIDTH}px solid {theme.INPUT_BORDER_COLOR};
            color: {theme.INPUT_FONT_COLOR};
            border-radius: {theme.INPUT_BORDER_RADIUS};
            padding: 5px;
        }}
        QTextEdit {{
            background-color: {theme.INPUT_BACKGROUND_COLOR};
            border: {theme.INPUT_BORDER_WIDTH}px solid {theme.INPUT_BORDER_COLOR};
            color: {theme.INPUT_FONT_COLOR};
            border-radius: {theme.INPUT_BORDER_RADIUS};
            padding: 5px;
        }}
        QLineEdit:disabled, QTextEdit:disabled, QCheckBox:disabled, QLabel:disabled {{
            color: {theme.INPUT_DISABLED_FONT_COLOR};
        }}

        QProgressBar {{
            border: 1px solid {theme.BORDER_HEAVY_COLOR};
            border-radius: {theme.PROGRESS_BAR_RADIUS}px;
            background-color: {theme.PROGRESS_BAR_BACKGROUND};
            text-align: center;
            font-size: 10pt;
            color: {theme.FONT_COLOR};
        }}
        QProgressBar:chunk {{
        }}



        
        QTabWidget {{
            background-color: {theme.BACKGROUND_COLOR};
        }}
        QTabWidget::pane {{
            border: none;
        }}
        QTabBar {{ /* Tab background */
            background-color: {theme.INACTIVE_BACKGROUND_COLOR};
            border-top: none;
            border-bottom: {theme.TAB_BORDER_WIDTH}px solid {theme.BORDER_HEAVY_COLOR};
        }}
        QTabBar::tab {{
            background-color: {theme.INACTIVE_BACKGROUND_COLOR};
            color: {theme.FONT_COLOR};
            min-width: {theme.TAB_MIN_WIDTH}px;
            padding: 5px 10px;
            margin-top: 3px;
            border-top-left-radius: {theme.TAB_BORDER_RADIUS}px;
            border-top-right-radius: {theme.TAB_BORDER_RADIUS}px;
            border-left: {theme.TAB_BORDER_WIDTH}px solid {theme.TAB_BORDER_COLOR};
            border-top: {theme.TAB_BORDER_WIDTH}px solid {theme.TAB_BORDER_COLOR};
            border-bottom: {theme.TAB_BORDER_WIDTH}px solid {theme.BORDER_HEAVY_COLOR};
            border-right: {theme.TAB_BORDER_WIDTH}px solid {theme.TAB_BORDER_COLOR};
        }}
        QTabBar::tab:hover {{
            background-color: {theme.HOVER_BACKGROUND};
            color: {theme.HOVER_FONT_COLOR};
        }}
        QTabBar::tab:selected {{
            color: {theme.TAB_ACTIVE_FONT_COLOR};
            background-color: {theme.TAB_ACTIVE_BACKGROUND_COLOR};
            margin-top: 0;
            border-bottom: {theme.TAB_BORDER_WIDTH}px solid {theme.TAB_ACTIVE_BORDER_BOTTOM};
        }}
        QTabBar::tab:last {{
            border-right: {theme.TAB_BORDER_WIDTH}px solid {theme.TAB_BORDER_COLOR};
        }}

        
        QToolBar {{
            background-color: {theme.TOOLBAR_BACKGROUND_COLOR};
            border-radius: {theme.TOOLBAR_RADIUS}px;
        }}
        QToolBar QToolButton {{
            background-color: transparent;
            border-radius: {theme.TOOLBAR_RADIUS};
        }}
        QToolButton:hover {{
            background-color: {theme.HOVER_BACKGROUND};
            color: {theme.HOVER_FONT_COLOR};
        }}


        .BottomToolbar:QToolBar {{
            background-color: {theme.TOOLBAR_BACKGROUND_COLOR};
            border-radius: {theme.TOOLBAR_RADIUS}px {theme.TOOLBAR_RADIUS}px  0px 0px;
        }}
        .BottomToolbar QLabel {{
            background: none;
        }}
        .BottomToolbar QToolButton {{
            background-color: none;
            color: {theme.BUTTON_DISABLED_FONT_COLOR};
            margin: 1px;
            border: {theme.SELECTION_BORDER_WIDTH}px solid transparent;
            padding: 2px;
        }}
        .BottomToolbar QToolButton:hover {{
            background-color: {theme.HOVER_BACKGROUND};
            color: {theme.HOVER_FONT_COLOR};
        }}
        .BottomToolbar QToolButton:checked {{
            background-color: {theme.SELECTION_BG_COLOR};
            color: {theme.SELECTION_FONT_COLOR};
            border: {theme.SELECTION_BORDER_WIDTH}px solid {theme.SELECTION_BORDER_COLOR};
        }}
        

        
        QTreeWidget, QTableView {{
            border: 2px solid {theme.BORDER_HEAVY_COLOR};
            border-radius: {theme.TOOLBAR_RADIUS}px;
        }}

        QHeaderView::section {{
            background-color: {theme.TABLE_HEAD_BACKGROUND_COLOR};
            color: {theme.FONT_COLOR};
            border: 2px solid {theme.BORDER_LIGHT_COLOR};
            border-left-color: transparent;
            border-top-color: transparent;
            border-bottom-color: transparent;
        }}
        QHeaderView::section:last {{
            border-right-color: transparent;
        }}


        QTreeView, QTableView {{
            alternate-background-color: {theme.TABLE_ROW_ALTERNATE_BACKGROUND};
            color: {theme.TABLE_ROW_FONT_COLOR};
        }}

        QTableView QTableCornerButton::section {{
            background-color: {theme.TABLE_HEAD_BACKGROUND_COLOR};
        }}

        QTreeView::item:hover, QTableView::item:hover {{
            background-color: {theme.HOVER_BACKGROUND};
            color: {theme.HOVER_FONT_COLOR};
        }}

        QTreeView::item:selected, QTableView::item:selected {{
            background-color: {theme.SELECTION_BG_COLOR};
            color: {theme.SELECTION_FONT_COLOR};
        }}

        QTreeView::item:active, QTableView::item:selected {{
            outline: none;
        }}


        
        

        QScrollBar {{
            background: {theme.SCROLLBAR_BACKGROUND};
        }}
        QScrollBar::handle {{
            background: {theme.SCROLLBAR_HANDLE};
            border-radius: {round(theme.SCROLLBAR_HANDLE_W*0.5)}px;
        }}
        QScrollBar:vertical {{
            width: {theme.SCROLLBAR_WIDTH}px;
            margin: 15px 0px 15px 0;
        }}
        QScrollBar::handle:vertical {{
            min-height: 40px;
            width: {theme.SCROLLBAR_HANDLE_W}px;
            margin: 0 {(theme.SCROLLBAR_WIDTH-theme.SCROLLBAR_HANDLE_W)//2}px;
        }}
        QScrollBar::handle:vertical:hover, QScrollBar::handle:vertical:active {{
            width: {theme.SCROLLBAR_WIDTH-6}px;
            margin: 0 3px;
        }}

        QScrollBar:horizontal {{
            height: {theme.SCROLLBAR_WIDTH}px;
            margin: 0 15px 0 15px;
        }}
        QScrollBar::handle:horizontal {{
            min-width: 40px;
            height: {theme.SCROLLBAR_HANDLE_W}px;
            margin: {(theme.SCROLLBAR_WIDTH-theme.SCROLLBAR_HANDLE_W)//2}px 0;
        }}
        QScrollBar::handle:horizontal:hover, QScrollBar::handle:horizontal:active {{
            height: {theme.SCROLLBAR_WIDTH-6}px;
            margin: 3px 0;
        }}
        QScrollBar::add-line:horizontal {{
            width: 15px;
            subcontrol-position: right;
            subcontrol-origin: margin;
            border: 0px solid black;
        }}

        QScrollBar::sub-line:horizontal {{
            width: 15px;
            subcontrol-position: left;
            subcontrol-origin: margin;
            border: 0px solid black;
        }}


        QScrollBar::add-page, QScrollBar::sub-page {{
            background: none;
        }}

        QScrollBar::add-line:vertical {{
            height: 15px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            color: white;
            border: 0 solid black;
        }}

        QScrollBar::sub-line:vertical {{
            height: 15px;
            subcontrol-position: top;
            subcontrol-origin: margin;
            color: white;
            border: 0 solid black;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {{
            border: 2px solid grey;
            width: 3px;
            height: 3px;
            background: white;
        }}

        
        QComboBox {{
            border: {theme.INPUT_BORDER_WIDTH}px solid {theme.INPUT_BORDER_COLOR};
            border-radius: {theme.INPUT_BORDER_RADIUS}px;
            padding: 1px 18px 1px 3px;
            min-width: 6em;
        }}
        QComboBox:editable {{
            background-color: {theme.INPUT_BACKGROUND_COLOR};
            color: {theme.INPUT_FONT_COLOR};
        }}
        QComboBox QAbstractItemView {{
            border-bottom-left-radius: {theme.INPUT_BORDER_WIDTH}px solid {theme.INPUT_BORDER_COLOR};
            border-bottom-right-radius: {theme.INPUT_BORDER_WIDTH}px solid {theme.INPUT_BORDER_COLOR};
            selection-background-color: lightgray;
        }}

        .setting-row {{
            background-color: red;
            color: white;
        }}
    """