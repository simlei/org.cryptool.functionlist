#!/usr/bin/env python3

import sys
import argparse
import flist
import dataclasses; from dataclasses import dataclass, field
from pathlib import Path
import flist_argtype as argtype
import flist_config as config
import flist_io as io

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


def CreateFinalForm(inputs, output):
    io.msg(f"converting into final format output {output} from files {inputs}")
    dataframe = flist.MCSV_Dataset.Dataframe_From_Files(inputs)
    mcsv_set = flist.MCSV_Dataset.From_Dataframe(dataframe)
    finalForm = flist.FinalForm_Dataset.From_MCSV(mcsv_set)

    finalForm.write_csv(output)

def argparse_contribute(parser, state: config.FlistProgramState):
    parser.add_argument("inputs", type=argtype.FilePathExisting, default=state.defaults.tofinalform.inputs, nargs="*")
    parser.add_argument("--output"  , type=argtype.FilePath        , default=state.defaults.tofinalform.output, nargs="?")

if __name__ == "__main__":
    parsed, flist_state = config.parse_args(sys.argv[1:], argparse_contribute)
    try:
        CreateFinalForm(parsed.inputs, parsed.output)
    except io.FlistException as e:
        io.err(str(e), e)
        exit(1)
