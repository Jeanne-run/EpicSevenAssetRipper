from .threads        import Worker, ThreadPool
from app.util.thread import ThreadData

class QtThreadedProcess(ThreadData):
    def __init__(self, pack, function, *args, **kwargs):
        self.pack = pack
        self.fn = function
        self.args = args
        self.kwargs = kwargs

    def set_worker(self):
        # Pass the function to execute
        self.worker    = Worker(self.fn, *self.args, thread=self, **self.kwargs)
        self.start     = self.worker.signals.start.emit
        self.finished  = self.worker.signals.finished.emit
        self.result    = self.worker.signals.result.emit
        self.progress  = self.worker.signals.progress.emit
        self.error     = self.worker.signals.error.emit

    def bind_listeners(self):

        self.worker.signals.start.connect( self.onstart )
        self.worker.signals.finished.connect( self.onfinished )
        self.worker.signals.progress.connect( self.onprogress )
        self.worker.signals.result.connect( self.onresult )
        self.worker.signals.error.connect( self.onerror )

    def remove_listeners(self):
        self.worker.signals.start.disconnect( )
        self.worker.signals.finished.disconnect( )
        self.worker.signals.progress.disconnect( )
        self.worker.signals.result.disconnect( )
        self.worker.signals.error.disconnect( )

    def run(self):
        self.set_worker()
        self.bind_listeners()

        # Execute
        ThreadPool.start(self.worker)

    def setStatus(self, *args):
        self.worker.signals.progress.emit( *args )