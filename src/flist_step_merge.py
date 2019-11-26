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


def Merge(files, output):

    scsv_dataframe = get_input_dataframe(files)
    scsv_all       = flist.SCSV_Dataset.From_Dataframe(scsv_dataframe)
    merged_entries = [Merged_Functionality(functionality = func) for func in [entry.functionality for entry in scsv_all]]

    for scsv_entry in scsv_all.get_entries():
        merge_targets = [entry for entry in merged_entries if entry.functionality == scsv_entry.functionality]
        if len(merge_targets) == 0 : raise Exception(f"no merge targets found for {scsv_entry}")
        if len(merge_targets) > 1  : raise Exception(f"multiple merge targets found for {scsv_entry}: {merge_targets}")
        for target in merge_targets:
            target.merge_with(scsv_entry)
        
    mcsv = merged_entries.to_MCSV()
    mcsv.to_dataframe().write_csv(output)


argparser = argparse.ArgumentParser()
argparser.add_argument("files"   , type=argtype.FilePathExisting, nargs="+")
argparser.add_argument("--output", type=argtype.FilePath)

if __name__ == "__main__":
    parsed = argparser.parse_args()
    Merge(parsed.files, parsed.output)
