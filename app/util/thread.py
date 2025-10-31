def nothing(*args):
    pass

class ThreadData:
    _abort: bool = False

    # listeners / connect
    onstart      = nothing
    onprogress   = nothing
    onfinished   = nothing
    onresult     = nothing
    onerror      = nothing
    
    # set other stuff here...

    def __init__(self):
        pass

    @staticmethod
    def remove_emits(cls) -> None:
        cls.progress = nothing
        cls.finished = nothing
        cls.result = nothing
        cls.error = nothing

    def is_stopping(self) -> bool:
        return self._abort

    def stop(self) -> None:
        self._abort = True

    def start(self, *args):
        self.onstart(*args)

    def progress(self, *args):
        self.onprogress(*args)

    def finished(self, *args):
        self.onprogress(*args)

    def result(self, *args):
        self.onprogress(*args)

    def error(self, *args):
        self.onprogress(*args)