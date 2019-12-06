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
import flist_api as api

import benedict; from benedict import benedict as bdict



def MergeImpl(files, output):

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


@dataclass
class MergeProg():

    inpaths: List[Path]
    outpath: Path
    strdict: dict

    def Main(self):
        return MergeImpl(self.inpaths, self.outpath)


class MergeSignature(api.ArgdictSignature):

    def get_varargs_id(self):
        return "input"

    def make_rawparse_spec(self) -> api.RawParse_Spec:
        spec = api.RawParse_Spec()
        spec.kw_ids = ["output"]
        spec.any_keywords_allowed = False
        return spec

    def make_default_argdict(self) -> dict:
        return {
            "input": [],
            "output": None
        }

    def convert_strdict(self, strdict: dict):
        print(f"converting strdict: {strdict}")
        bd = bdict(strdict)
        inputstrings = api.require_arg_key(strdict, "input", list)
        outputstring = api.require_arg_key(strdict, "output", str)
        if len(inputstrings) == 0:
            raise api.ApiException("zero input files are not allowed")
        inpaths = [argtype.FilePathExisting(path) for path in inputstrings]
        outpath = argtype.FilePath(outputstring)
        return MergeProg(inpaths, outpath, strdict)

signature = MergeSignature()

if __name__ == "__main__":
    prog = signature.parse(signature, sys.args)
    prog.Main()

