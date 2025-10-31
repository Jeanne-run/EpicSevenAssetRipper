from typing import TypedDict, LiteralString, Optional, Self, List, Union

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