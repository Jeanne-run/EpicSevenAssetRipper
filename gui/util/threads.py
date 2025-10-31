from PyQt6.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
import traceback, sys

ThreadPool = QThreadPool()

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        tuple
            0 = int indicating % progress
            1 = text for label

    '''
    start = pyqtSignal(tuple)
    finished = pyqtSignal(tuple)
    error = pyqtSignal(tuple, tuple)
    result = pyqtSignal(tuple, object)
    progress = pyqtSignal(tuple)
    do_main = pyqtSignal(object, tuple)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            self.signals.start.emit( self.args )
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit( self.args, (exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit( self.args, result )  # Return the result of the processing
        finally:
            self.signals.finished.emit( self.args )  # Done
