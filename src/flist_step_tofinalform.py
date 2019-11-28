#!/usr/bin/env python3

import sys
import argparse
import flist
import dataclasses; from dataclasses import dataclass, field
from pathlib import Path
import flist_argtype as argtype

@dataclass
class HTMLTemplates:
    dir: Path
    template_interactive: Path = field(init=False)
    fragment_row: Path         = field(init=False)
    fragment_category: Path    = field(init=False)

    def __post_init__(self):
        self.template_interactive = self.dir / "template_interactive.html"
        self.fragment_row         = self.dir / "fragment_row.html"
        self.fragment_category    = self.dir / "fragment_category.html"


def CreateFinalForm(input_mcsv, output):
    dataframe = flist.MCSV_Dataset.Dataframe_From_File(input_mcsv, flist.MCSV_Dataset.COLUMNS)
    mcsv_set = flist.MCSV_Dataset.From_Dataframe(dataframe)
    finalForm = flist.FinalForm_Dataset.From_MCSV(mcsv_set)

    finalForm.write_csv(output)





if __name__ == "__main__":
    flist_state, restargs = flist.FlistProgramState.ParseStateFromArgs(sys.argv[1:])

    argparser = argparse.ArgumentParser()
    argparser.add_argument("input_mcsv", type=argtype.FilePathExisting, default=flist_state.fs.workspace / "all_merged.csv", nargs="?")
    argparser.add_argument("--output"  , type=argtype.FilePath        , default=flist_state.fs.workspace / "all_final.csv" , nargs="?")
    parsed = argparser.parse_args(restargs)

    CreateFinalForm(parsed.input_mcsv, parsed.output)
