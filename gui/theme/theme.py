from app     import settings
from .styles import DarkTheme, LightTheme, RoundedLightTheme, RoundedDarkTheme, AccentColorDarkTheme, apply

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
            return AccentColorDarkTheme

def use_theme(app, val=settings.getTheme()):
    theme = get_theme_scheme(val)

    app.ThemeColors = theme
    app.setStyleSheet(apply(theme))