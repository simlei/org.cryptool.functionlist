#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype

import flist

def get_input_dataframe(files):
    if len(files) == 0: raise Exception("empty: scsv files")
    frames = [flist.SCSV_Dataset.Dataframe_From_File(file) for file in files]
    return pandas.concat(frames)



# Just for illustration purpose -- it's reversible (but not resistant to bad manual edits that exceed whitespace around csv delims)
def Unmerge(file):
    unmerged = flist.MCSV_Dataset.From_Dataframe(flist.MCSV_Dataset.Dataframe_From_File(file, flist.MCSV_Dataset.COLUMNS))
    print(unmerged.rows[0])

def Merge(files, output):
    scsv_dataframe = get_input_dataframe(files)
    scsv_all       = flist.SCSV_Dataset.From_Dataframe(scsv_dataframe)
    merged_rows = [flist.Merged_Functionality(functionality) for functionality in scsv_all.get_functionalities()]

    for scsv_row in scsv_all.get_rows():
        merge_targets = [merged for merged in merged_rows if merged.functionality == scsv_row["functionality"]]
        if len(merge_targets) == 0 : raise Exception(f"no merge targets found for {scsv_row}")
        if len(merge_targets) > 1  : raise Exception(f"multiple merge targets found for {scsv_row}: {merge_targets}")
        for target in merge_targets:
            target.merge_with(scsv_row)
        
    mcsv_rows = [ merged.to_MCSV() for merged in merged_rows ]
    mcsv_all = flist.MCSV_Dataset.From_Rows(mcsv_rows)
    mcsv_all.write_csv(output)


if __name__ == "__main__":
    flist_state, restargs = flist.FlistProgramState.ParseStateFromArgs(sys.argv[1:])

    argparser = argparse.ArgumentParser()
    argparser.add_argument("input_scsv"   , type=argtype.FilePathExisting, nargs="*", default=list(flist_state.fs.workspace.glob("data/scsv_webdump/*.csv")))
    argparser.add_argument("--output", type=argtype.FilePath, default=flist_state.fs.workspace / "all_merged.csv")
    parsed = argparser.parse_args()
    Merge(parsed.input_scsv, parsed.output)
