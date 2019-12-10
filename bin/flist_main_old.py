#!/usr/bin/env python3

import plumbum; from plumbum import local
import argparse
import sys
import subprocess
import flist_io as io
import typing; from typing import List, Dict, Any, Optional
import dataclasses; from dataclasses import dataclass, field

import flist_api as api
import flist_steps as steps
import flist_files

from plumbum.commands import BaseCommand
    

def runMainStepSequence(ws):
    flist_files.workspace = ws
    flist_files.refresh_workspace()

    steps.CT2scsv_ct2_en.makeprog(ws).Main()
    steps.CT2scsv_ct2_de.makeprog(ws).Main()
    steps.CT2scsv_jct_en.makeprog(ws).Main()
    steps.CT2scsv_jct_de.makeprog(ws).Main()

    steps.categories_ct2_en.makeprog(ws).Main()
    steps.categories_ct2_de.makeprog(ws).Main()
    steps.categories_jct_en.makeprog(ws).Main()
    steps.categories_jct_de.makeprog(ws).Main()

    steps.merge_en.makeprog(ws).Main()
    steps.merge_de.makeprog(ws).Main()

    steps.tofinalform_en.makeprog(ws).Main()
    steps.tofinalform_de.makeprog(ws).Main()

    steps.tohtml_en.makeprog(ws).Main()

if __name__ == "__main__":
    mainprog = sys.argv[0]
    restargs = []
    workspace = flist_files.workspace
    for arg in sys.argv[1:]:
        if (ws_arg := arg.replace("-workspace=")) != arg:
            workspace = Path(ws_arg)
        else:
            restargs.append(arg)

    if(len(restargs) == 0):
        runMainStepSequence(workspace)
        exit(0)
    else:
        exit(1)
