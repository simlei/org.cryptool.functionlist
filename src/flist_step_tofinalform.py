#!/usr/bin/env python3

import sys
import argparse
import flist
import dataclasses; from dataclasses import dataclass, field
from pathlib import Path
import flist_argtype as argtype
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


def CreateFinalForm(input: Path, output: Path):
    inputs = [ input ]
    io.msg(f"converting into final format output {output} from files {inputs}")
    dataframe = flist.MCSV_Dataset.Dataframe_From_Files(inputs)
    mcsv_set = flist.MCSV_Dataset.From_Dataframe(dataframe)
    finalForm = flist.FinalForm_Dataset.From_MCSV(mcsv_set)

    finalForm.write_csv(output)
