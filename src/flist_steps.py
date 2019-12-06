import flist_api as api
import flist_config as config
from pathlib import Path
import dataclasses; from dataclasses import dataclass, field
import typing; from typing import List, Dict, Any, Callable, Optional
import sys
import subprocess

import plumbum; from plumbum.commands import BaseCommand

def RunStep(step_prog) -> bool:
    io.msg(f"Running step: {step_prog}")
    currentStep = step_prog
    proc = step_prog.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); 
    currentProc = proc
    proc.communicate(); 
    if proc.returncode != 0: 
        return False
    else:
        return True

@dataclass
class FlistPyEntrypoint:
    module: Any
    init_args: List[str] = field(default_factory=list)
    sig: api.ArgdictSignature = field(default=None)

    def __post_init__(self):
        self.sig = self.module.signature

    def makeprog(self, additionalArgs: List[str]):
        args = self.init_args.copy()
        args = args + additionalArgs
        print(additionalArgs) # dbg
        prog = self.sig.parse([str(self)] + additionalArgs)
        return prog
    
def flist_augment_cfgpath(ws: Path, cfgpath: str):
    if cfgpath.startswith("."):
        return ws / cfgpath
    else:
        return Path(cfgpath)

@dataclass
class FlistStepCmd:
    id: str
    entrypoint: FlistPyEntrypoint
    
    def makeprog(self, ws: Path) -> api.ArgdictArgs:
        additionalArgs = []
        config_dict = config.require_cfg(self.id)
        for k,v in config_dict.items():
            if isinstance(v, list):
                augmentedpaths = [flist_augment_cfgpath(ws, p) for p in v]
                for p in augmentedpaths:
                    # additionalArgs.extend([f"--{k}+={p.as_posix()}" for p in augmentedpaths])
                    isKv = self.entrypoint.sig.is_keyval_id(k)
                    print(self.entrypoint.sig.get_positional_ids())
                    print(f"{(k,p)=} {isKv=}")
                    strRep = p.as_posix()
                    if isKv:
                        additionalArgs.append(f"--{k}={strRep}")
                    else:
                        additionalArgs.append(f"{strRep}")
            else:
                if k == "output":
                    v = flist_augment_cfgpath(ws, v)
                if isinstance(v, Path):
                    strRep = v.as_posix()
                else:
                    strRep = str(v)
                
                isKv = self.entrypoint.sig.is_keyval_id(k)
                # print(f"{(k,v)=} {isKv=}")
                if isKv:
                    additionalArgs.append(f"--{k}={strRep}")
                else:
                    additionalArgs.append(f"{strRep}")
                
        return self.entrypoint.makeprog(additionalArgs)


import flist_workspace

import flist_step_CT2scsv
import flist_step_categories
import flist_step_merge
import flist_step_tofinalform
import flist_step_tohtml

prog_ct2scsv = FlistPyEntrypoint(flist_step_ct2scsv)
prog_categories = FlistPyEntrypoint(flist_step_categories)
prog_merge = FlistPyEntrypoint(flist_step_merge)
prog_tofinalform = FlistPyEntrypoint(flist_step_tofinalform)
prog_tohtml = FlistPyEntrypoint(flist_step_tohtml)

# The actual steps
CT2scsv_ct2_en = FlistStepCmd("CT2scsv_ct2_en", prog_ct2scsv)
CT2scsv_ct2_de = FlistStepCmd("CT2scsv_ct2_de", prog_ct2scsv)
CT2scsv_jct_en = FlistStepCmd("CT2scsv_jct_en", prog_ct2scsv)
CT2scsv_jct_de = FlistStepCmd("CT2scsv_jct_de", prog_ct2scsv)

categories_ct2_en = FlistStepCmd("categories_ct2_en", prog_categories)
categories_ct2_de = FlistStepCmd("categories_ct2_de", prog_categories)
categories_jct_en = FlistStepCmd("categories_jct_en", prog_categories)
categories_jct_de = FlistStepCmd("categories_jct_de", prog_categories)

merge_en = FlistStepCmd("merge_en", merge_prog)
merge_de = FlistStepCmd("merge_de", merge_prog)

tofinalform_en = FlistStepCmd("tofinalform_en", prog_tofinalform)
tofinalform_de = FlistStepCmd("tofinalform_de", prog_tofinalform)

tohtml_en = FlistStepCmd("tohtml_en", prog_tohtml)

print(step_merge_en.makeprog(config.project_root / "ws"))
