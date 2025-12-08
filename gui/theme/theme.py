from app     import settings
from .styles import DarkTheme, LightTheme, RoundedLightTheme, RoundedDarkTheme, AccentColorDarkTheme, apply

USE_THEME = DarkTheme

THEMES = [
    'light',
    'light-r',
    'dark',
    'dark-r',
    'dark-accent'
]

def get_theme_scheme(value: str):
    match(value):
        case 'light':
            return LightTheme
        case 'light-r':
            return RoundedLightTheme
        case 'dark':
            return DarkTheme
        case 'dark-r':
            return RoundedDarkTheme
        case 'dark-accent':
            return AccentColorDarkTheme
        case _:
            return RoundedDarkTheme

def use_theme(app, val=settings.getTheme()):
    global USE_THEME
    USE_THEME = get_theme_scheme(val)

    app.ThemeColors = USE_THEME
    app.setStyleSheet(apply(USE_THEME))