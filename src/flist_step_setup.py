#!/usr/bin/env python3

import os
import sys
import flist
import shutil
import argparse; from argparse import FileType
import flist_argtype as argtype
import flist_config as config
import pathlib; from pathlib import Path
import flist_io as io

def CreateFreshWorkspace(state: config.FlistProgramState):
    if state.fs.workspace.exists():
        shutil.rmtree(state.fs.workspace)
    os.makedirs(state.fs.workspace)

    io.msg(f"populating workspace: {state.fs.workspace}")
    for subelement in state.fs.ws_static_content_dir.glob("*"):
        shutil.copytree(subelement, state.fs.workspace / subelement.relative_to(state.fs.ws_static_content_dir))
    io.msg(f"Flist workspace and data initialized to: {state.fs}")
    io.verbose(f"Flist defaults initilized to: {state.defaults}")

if __name__ == "__main__":
    # required no special arguments other than the workspace
    parsed, flist_state = config.parse_args(sys.argv[1:], lambda parser,state: None)
    try:
        CreateFreshWorkspace(flist_state)
    except io.FlistException as e:
        io.err(e.msg, e)
        exit(1)

