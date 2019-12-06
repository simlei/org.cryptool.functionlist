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


if __name__ == "__main__":
    # required no special arguments other than the workspace
    parsed, flist_state = config.parse_args(sys.argv[1:], lambda parser,state: None)
    try:
        CreateFreshWorkspace(flist_state)
    except io.FlistException as e:
        io.err(str(e), e)
        exit(1)

