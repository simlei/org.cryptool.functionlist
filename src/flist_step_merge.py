#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype
import flist_config as config

import dataclasses; from dataclasses import dataclass
import typing; from typing import List, Dict, Any

import flist
import flist_io as io
import flist_api as api; from flist_api import implicitly

import benedict; from benedict import benedict as bdict


def MergeImpl(input: List[Path], output: Path):

    implicitly("prog.logger").debug(f"Running MergeImpl({input=}, {output=})")
    scsv_dataframe = flist.SCSV_Dataset.Dataframe_From_Files(input)
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

