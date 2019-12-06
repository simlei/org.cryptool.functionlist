import argparse
import flist_api as api
import pathlib; from pathlib import Path

def PathNonexisting(s: str) -> Path:
    path = Path(s)
    if(path.exists()):
        raise api.ApiException(f"path {s} already exists")
    return path

def FilePathExisting(s: str) -> Path:
    path = Path(s)
    if(path.exists() and not path.is_file()):
        raise api.ApiException(f"path {s} exists and is not a regular file")
    if(not path.exists()):
        raise api.ApiException(f"path {s} does not exist")
    return path

def FilePath(s: str) -> Path:
    path = Path(s)
    if(path.exists() and not path.is_file()):
        raise api.ApiException(f"path {s} exists and is not a regular file")
    return path

def DirPathExisting(s: str) -> Path:
    path = Path(s)
    if(path.exists() and not path.is_dir()):
        raise api.ApiException(f"path {s} exists and is not a directory")
    if(not path.exists()):
        raise api.ApiException(f"path {s} does not exist")
    return path

def DirPath(s: str) -> Path:
    path = Path(s)
    if(path.exists() and not path.is_dir()):
        raise api.ApiException(f"path {s} exists and is not a directory")
    return path
