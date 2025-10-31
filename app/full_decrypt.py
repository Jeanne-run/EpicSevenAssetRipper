from app.util.tree    import PackFileScanner
from .pack            import DataPack
from .util.thread     import ThreadData
from .util.misc       import FileDescriptor
from .util.exceptions import OperationAbortedByUser
from .util.tree       import create_file
from .load_hooks      import call_hooks
import os

def decrypt_and_write(pack: DataPack, dest: str, thread: ThreadData):
    b = 0
    chunkSize = 100000
    pr = 0
    l = os.path.getsize(pack.get_path()) 
    with open(pack.get_path(), 'rb') as f:
        with open(dest, 'wb') as w:
            while True:
                if thread.is_stopping():
                    break

                p = round(b/l*100)
                if p>pr:
                    thread.progress((p,))
                    pr = p

                data = pack.read_bytes(f, b, chunkSize)
                if len(data) == 0:
                    break
                b+=len(data)
                w.write( bytes(data) )



def extract_all(pack: DataPack, dest: str, thread: ThreadData):
    file = PackFileScanner(pack)
    mmap = pack.mmap()
    p = 0
    s = mmap.size()

    while True:
        if thread.is_stopping():
            raise OperationAbortedByUser('')
        
        member = file.next()

        if member is None:
            break

        _p = round(member.offset_data/s*100)
        if _p>p:
            thread.progress((_p,))
            p = _p

        n = os.path.split(member.name)

        if n[0] != '':
            dir = os.path.join(dest, n[0])
            os.makedirs(dir, exist_ok=True)

        path = os.path.join(dest, member.name)

        file_dict = create_file(name=n[1], full_name=member.name, size=member.size, offset=member.offset_data)

        data = file.get_file_content(file_dict)

        # mmap.seek(member.offset_data)

        # data = pack.read_bytes(mmap, member.offset_data, member.size)
        
        _file = FileDescriptor(data=data, path=path, tree_file=file_dict, pack=pack, thread=thread)

        call_hooks('before', _file)

        if _file.path is not None:
            with open(_file.path, 'wb') as f:
                f.write(_file.bytes)
                _file.written = True

        call_hooks('after', _file)