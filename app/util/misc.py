import functools
from dataclasses import dataclass
from threading   import Timer
from typing      import TYPE_CHECKING

if TYPE_CHECKING:
    from .bytearray  import ByteArray
    from .types      import FileType
    from .thread     import ThreadData
    from ..pack      import DataPack
else:
    ByteArray = None
    FileType = None
    ThreadData = None
    DataPack = None


@dataclass(init=False, eq=False, match_args=False)
class FileDescriptor:
    path: str = None
    bytes: ByteArray = None
    tree_file: FileType = None
    pack: DataPack = None
    thread: ThreadData = None
    written: bool = False

    def __init__(self, data: ByteArray, path: str, tree_file: FileType, pack: DataPack, thread: ThreadData):
        self.path = path
        self.bytes = data
        self.tree_file = tree_file
        self.pack = pack
        self.thread = thread


def debounce(timeout: float):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.func.cancel()
            wrapper.func = Timer(timeout, func, args, kwargs)
            wrapper.func.start()
        
        wrapper.func = Timer(timeout, lambda: None)
        return wrapper
    return decorator