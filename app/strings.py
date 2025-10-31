from . import settings

LOCALES = [
    'en',
    'it'
]

STRINGS = {}
LOCALE = 'en'

def setLocale(locale: str = LOCALE):
    global LOCALE, STRINGS
    try:
        match locale:
            case 'it':
                from i18n.it import IT
                STRINGS = IT
            case 'en':
                from i18n.en import EN
                STRINGS = EN
            case _:
                raise Exception()
        LOCALE = locale
    except Exception: # Fallback to english
        try:
            from i18n.en import EN # Fallback to en
            STRINGS = EN
            settings.setLanguage('en')
        except Exception as e:
            print(e)

@staticmethod
def translate(key: str, *args, **kwargs):
    try:
        return getattr(STRINGS, key)
    except Exception:
        return key