import os
import sys
import flist
import shutil
import glob
import scriptlib; from scriptlib import Arg, Args, Scriptspec
import plumbum; from plumbum import local
import dataclasses; from dataclasses import dataclass

srcfolder = os.path.dirname(__file__)
def script_in_src(basename):
    return os.path.join(srcfolder, basename)

setup           = local["flist_step_setup.py"]
# scsv_CT2        = local["flist_step_CT2_to_scsv.py"]
merge_scsv      = local["flist_step_merge.py"]
wscopy          = local["workspace_copy.py"]

@dataclass
class FListComponents:
    workspace: str

    def ws_arg(self):
        return f"--workspace={self.workspace}"

    def __post_init__(self):
        self.step_setup      = setup[self.ws_arg()]
        # self.step_scsv_ct2   = scsv_ct2[self.ws_arg()]
        self.step_merge_scsv = merge_scsv[self.ws_arg()]

        self.wscopy          = wscopy


