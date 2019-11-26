#!/usr/bin/env python3

import os
import sys
import flist
import shutil
import argparse; from argparse import FileType
import flist_argtype as argtype

def CreateFreshWorkspace(workspace, data):
    print(f"FList: working with: {workspace=}, {data=}")
    if os.path.exists(workspace):
        shutil.rmtree(workspace)
    os.makedirs(workspace)

    shutil.copytree(data, os.path.join(workspace, "data"))

argparser = argparse.ArgumentParser()
argparser.add_argument("workspace", type=argtype.DirPath        , default=str(flist.dev_state.fs.workspace), nargs="?")
argparser.add_argument("--datadir", type=argtype.DirPathExisting, default=str(flist.dev_state.fs.datadir))

if __name__ == "__main__":
    parsed = argparser.parse_args()
    CreateFreshWorkspace(parsed.workspace, parsed.datadir)

