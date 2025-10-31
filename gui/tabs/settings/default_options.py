from app.strings import translate, LOCALES
from app.settings  import (
    getLanguage, setLanguage,
    getStopOnClose, setStopOnClose,
    getAutosaveFileTree, setAutosaveFileTree,
    getAutomaticFilePreview, setAutomaticFilePreview,
    getTheme, setTheme, 
    getDefaultFilePromptPath, setDefaultFilePromptPath)
from gui.theme.theme import THEMES

def getLocaleIndex(v):
    try:
        return LOCALES.index(v)
    except:
        return 0

def getThemeIndex(v):
    try:
        return THEMES.index(v)
    except:
        return 0


OPTIONS = [
    [translate('language'), translate('set_language_desc'), 'select', getLocaleIndex( getLanguage() ), [ translate(f'lang_{locale}') for locale in LOCALES], lambda i: setLanguage(LOCALES[i])],
    [translate('theme'), translate('set_theme_desc'), 'select', getThemeIndex( getTheme() ), THEMES, lambda i: setTheme(THEMES[i])],
    [translate('set_stop_on_main_close'), translate('set_stop_on_main_close_desc'), 'checkbox', getStopOnClose(), None, lambda v: setStopOnClose(v != 0)],
    [translate('set_automatic_file_preview'), translate('set_automatic_file_preview_desc'), 'checkbox', getAutomaticFilePreview(), None, lambda v: setAutomaticFilePreview(v != 0)],
    [translate('set_autosave_tree'), translate('set_autosave_tree_desc'), 'checkbox', getAutosaveFileTree(), None, lambda v: setAutosaveFileTree(v != 0)],
    [translate('set_default_file_prompt_path'), translate('set_default_file_prompt_path_desc'), 'path', getDefaultFilePromptPath(), translate('select'), lambda v: setDefaultFilePromptPath(v) if v!=None else 0]
]