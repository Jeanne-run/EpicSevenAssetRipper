from typing import TypedDict, Optional, List

try:
    from typing import Self, Literal
except ImportError:
    # Python <3.11 fallback definitions
    try:
        from typing_extensions import Self, Literal
    except ImportError:
        Self = None  # or just object
        Literal = None


class FileType(TypedDict):
    type: Literal['file']
    name: str
    full_path: str
    format: str
    offset: int
    size: int
    extra_bytes: Optional[List[int]]

class FolderType(TypedDict):
    type: Literal['folder']
    name: str
    size: int
    files: int
    children: List[Self | FileType]

FileTreeType = List[FolderType | FileType]