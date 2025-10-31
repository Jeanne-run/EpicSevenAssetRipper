import traceback

try:
    from gui.app    import CreateApp

    CreateApp()

except Exception as e:
    exception = traceback.format_exc()
    print(exception)
    with open('crash-report.txt', 'w') as f:
        f.write(exception)
        # traceback.TracebackException.from_exception(e).print(file=f)