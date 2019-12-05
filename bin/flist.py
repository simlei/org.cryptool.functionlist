#!/usr/bin/env python3

import flist_config as config
import plumbum; from plumbum import local
import argparse
import sys
import subprocess
import flist_io as io
import typing; from typing import List, Dict, Any

import api

# A step needs - a sub namespace
# - a sub parser
# - a contribution to the top parser: sub kw
@dataclass
class Step:
    
    config: api.Configuration # alias for Namespace



     
    
    


currentStep = None
currentProc = None
def RunStep(step_prog) -> bool:
    global currentStep 
    global currentProc
    io.msg(f"Running step: {step_prog}")
    currentStep = step_prog
    proc = step_prog.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); 
    currentProc = proc
    proc.communicate(); 
    if proc.returncode != 0: 
        return False
    else:
        return True


def FullRun(state):
    step_setup       = local.python[config.project_root / "src/flist_step_setup.py"] # type: local.LocalCommand
    step_ct2scsv     = local.python[config.project_root / "src/flist_step_CT2scsv.py"]["--"]
    step_ct2scsv     = local.python[config.project_root / "src/flist_step_CT2scsv.py"]
    # step_ct2scsv     = local.python[config.project_root / "src/flist_step_JCTscsv.py"]
    step_merge       = local.python[config.project_root / "src/flist_step_merge.py"]
    step_tofinalform = local.python[config.project_root / "src/flist_step_tofinalform.py"]
    step_tohtml      = local.python[config.project_root / "src/flist_step_tohtml.py"]

    # TODO: warum and
    successful = (
        RunStep(step_setup)       and 
        RunStep(step_ct2scsv)     and 
        RunStep(step_merge)       and 
        RunStep(step_tofinalform) and 
        RunStep(step_tohtml)      and 
        sys.exit()
    ) or (
        io.err(f"Unsuccessful run, aborted in step {currentStep}") or sys.exit(currentProc.returncode)
    )

    # proc = step_setup.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); proc.communicate(); 
    # if proc.returncode != 0: 
    #     sys.exit(proc.returncode)

    # proc = step_merge.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); proc.communicate(); 
    # if proc.returncode != 0: 
    #     sys.exit(proc.returncode)

    # proc = step_tofinalform.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); proc.communicate(); 
    # if proc.returncode != 0: 
    #     sys.exit(proc.returncode)

    # proc = step_tohtml.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); proc.communicate(); 
    # if proc.returncode != 0: 
    #     sys.exit(proc.returncode)

    # step_setup(f"--workspace={state.fs.workspace}")
    # step_merge(f"--workspace={state.fs.workspace}")
    # step_tofinalform(f"--workspace={state.fs.workspace}")

    # print(step_tohtml(f"--workspace={state.fs.workspace}"))


def argparse_contribute(parser: argparse.ArgumentParser, state: config.FlistProgramState):
    pass

if __name__ == "__main__":
    parsed, flist_state = config.parse_args(sys.argv[1:], argparse_contribute)
    FullRun(flist_state)
