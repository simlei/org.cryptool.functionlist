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

if __name__ == "__main__":
    flist_state, restargs = flist.FlistProgramState.ParseStateFromArgs(sys.argv)
    CreateFreshWorkspace(flist_state.fs.workspace, flist_state.fs.datadir)


