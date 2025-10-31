import os
from typing           import TYPE_CHECKING
from .load_hooks      import call_hooks
from .util.exceptions import OperationAbortedByUser
from .util.tree       import count_size_tree
from .util.pack_read  import PackFileScanner
from .util.misc       import FileDescriptor
from .util.types      import FileTreeType, FileType
from .util.thread     import ThreadData

if TYPE_CHECKING:
    from .pack        import DataPack
else:
    DataPack = None

def extract(pack: DataPack, files: FileTreeType, base_path: str, thread: ThreadData):

    if not isinstance(files, list):
        files = [files]

    packio = PackFileScanner(pack)

    file_size = count_size_tree(files)
    processed_files = 0
    progress_percentage = -1

    def recrusive_writing(path, files):
        nonlocal processed_files, progress_percentage, file_size
        for file in files:

            if thread.is_stopping():
                raise OperationAbortedByUser('Operation was interrupted by the user')

            if file['type'] == 'folder':
                ndir = os.path.join(path, file['name'])
                os.makedirs( ndir, exist_ok=True )
                recrusive_writing(ndir, file['children'])
            else:
                _pfiles = processed_files + file['size']
                _percentage = round( _pfiles / file_size *100)
                processed_files = _pfiles
                if _percentage > progress_percentage:
                    thread.progress((progress_percentage,file['full_path']))
                    progress_percentage = _percentage

                data = packio.get_file_content(file)
                file_path = os.path.join(path, file['name'])

                file = FileDescriptor(data=data, path=file_path, tree_file=file, pack=pack, thread=thread)

                call_hooks('before', file)

                if file.path:
                    with open(file.path, 'wb') as f:
                        f.write(file.bytes)
                        file.written = True

                call_hooks('after', file)


    recrusive_writing(base_path, files)

    packio.close()

    print('Done')

def get_file(file: FileType, pack: DataPack = None):
    reader = PackFileScanner(pack)
    bytes_ = reader.get_file_content(file)
    reader.close()
    f = FileDescriptor(data=bytes_, path=None,tree_file=file, pack=pack, thread=ThreadData())
    call_hooks('before', f)
    call_hooks('after', f)
    return f.bytes
