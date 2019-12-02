#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype
import flist_config as config

import flist
import flist_io as io


# Just for illustration purpose -- it's reversible (but not resistant to bad manual edits that exceed whitespace around csv delims)
def Unmerge(file):
    unmerged = flist.MCSV_Dataset.From_Dataframe(flist.MCSV_Dataset.Dataframe_From_File(file, flist.MCSV_Dataset.COLUMNS))
    print(unmerged.rows[0])

def Merge(files, output):
    io.msg(f"merging scsv files into {output}: {files}")
    scsv_dataframe = flist.SCSV_Dataset.Dataframe_From_Files(files)
    scsv_all       = flist.SCSV_Dataset.From_Dataframe(scsv_dataframe)
    merged_rows = [flist.Merged_Functionality(functionality) for functionality in scsv_all.get_functionalities()]

    for scsv_row in scsv_all.get_rows():
        merge_targets = [merged for merged in merged_rows if merged.functionality == scsv_row["functionality"]]
        if len(merge_targets) == 0 : raise io.FlistException(f"no merge targets found for {scsv_row}")
        if len(merge_targets) > 1  : raise io.FlistException(f"multiple merge targets found for {scsv_row}: {merge_targets}")
        for target in merge_targets:
            target.merge_with(scsv_row)
        
    mcsv_rows = [ merged.to_MCSV() for merged in merged_rows ]
    mcsv_all = flist.MCSV_Dataset.From_Rows(mcsv_rows)
    mcsv_all.write_csv(output)

def argparse_contribute(parser, state: config.FlistProgramState):
    parser.add_argument(
        "input", 
        type=argtype.FilePathExisting, 
        nargs="*", 
        default=state.defaults.merge.inputs
    )
    parser.add_argument("--output", 
                        type=argtype.FilePath, 
                        default=state.defaults.merge.output
                        )

if __name__ == "__main__":
    parsed, flist_state = config.parse_args(sys.argv[1:], argparse_contribute)

    try:
        Merge(parsed.input, parsed.output)
    except io.FlistException as e:
        io.err(str(e), e)
        exit(1)
