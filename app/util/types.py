from typing import TypedDict, Optional, List, Union

try:
    from typing import LiteralString, Self
except ImportError:
    # Python <3.11 fallback definitions
    LiteralString = str
    try:
        from typing_extensions import Self
    except ImportError:
        Self = None  # or just object


class FileType(TypedDict):
    type: LiteralString = 'file'
    name: str
    full_path: str
    format: str
    offset: int
    size: int
    extra_bytes: Optional[List[int]]

class FolderType(TypedDict):
    type: LiteralString = 'folder'
    name: str
    size: int
    files: int
    children: List[Self | FileType]

FileTreeType = List[FolderType | FileType]