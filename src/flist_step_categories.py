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

def Add_Categories(input: Path, catfile: Path, output: Path):
    implicitly("prog.logger").debug(f"running Add_Categories({input=}, {catfile=}, {output=})")
    pass
    # with open(input, "") as opened
