#!/usr/bin/env python3

import sys
import os

import pandas
import flist
from flist import *
import scriptlib; from scriptlib import Arg, Args, Scriptspec, expand_workspace_filelist


def get_input_dataframe(scsv_files):
    if len(scsv_files) == 0: raise Exception("empty: scsv files")
    frame = None
    for file in scsv_files:
        if frame is None:
            frame = SCSV_Dataset.Dataframe_From_File(file)
        else:
            frame = pandas.concat(frame, SCSV_Dataset.Dataframe_From_File(file))

    return frame


def Merge(files, output):

    scsv_dataframe = get_input_dataframe(scsv_files)
    scsv_all       = SCSV_Dataset.From_Dataframe(scsv_dataframe)
    merged_entries = [Merged_Functionality(functionality = func) for func in [entry.functionality for entry in scsv_all]]

    for scsv_entry in scsv_all.get_entries():
        print(scsv_entry)
        merge_targets = [entry for entry in merged_entries if entry.functionality == scsv_entry.functionality]
        if len(merge_targets) == 0 : raise Exception(f"no merge targets found for {scsv_entry}")
        if len(merge_targets) > 1  : raise Exception(f"multiple merge targets found for {scsv_entry}: {merge_targets}")
        for target in merge_targets:
            target.merge_with(scsv_entry)
        
    mcsv = merged_entries.to_MCSV()
    mcsv.to_dataframe().write_csv(output)

def Merge_ArgReceiver(workspace, files, output):
    _workspace = workspace[-1]
    _output    = output[-1]
    expanded = expand_workspace_filelist(_workspace, files)
    return Merge(
        expanded,
        os.path.join(_workspace, output)
    )

# Argument parsing{{{

script_handler = Scriptspec(
    __file__, 
    Args([
        Arg.Positional    ("files"               ), 
        Arg.Keyval        ("workspace"           ),
        Arg.Keyval        ("output"              )
    ]),
    self_passed_args = [
        "--output=merged_output.csv"
    ],
    kwargs_receiver = Merge_ArgReceiver,
)

if __name__ == "__main__":
    script_handler.run(sys.argv[1:])

# vim: fdm=marker
# }}}
