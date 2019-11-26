# vim: fdm=marker

from __future__ import annotations
from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass, field
import os
import re
import sys
import argparse
import pandas
from typing import List, Any
import pathlib; from pathlib import Path


# @dataclass
# class FlistFilesystem:
#     workspace: Path
#     datadir: Path

# @dataclass
# class FlistProgramState:
#     fs: FlistFilesystem

# dev_state = FlistProgramState(
#     FlistFilesystem(
#         workspace = Path(__file__).parent.parent / "ws",
#         datadir = Path(__file__).parent.parent / "data"
#     )
# )

# ---- Data specification{{{

# DCSV_CT2: CT2 dynamic csv-like data (different numbers of columns per line -> state based)
# SCSV: single csv -- all cells are atomar (no lists)
# MCSV: merged csv

CSV_SEP=";"

class CSV_Entry(ABC): # {{{
    pass

    # @abstractmethod
    # def as_dict(self) -> dict:
    #     pass
 # }}}
class CSV_Dataset(ABC): # {{{

    @abstractmethod
    def get_entries(self) -> List[CSV_Entry]:
        pass

    @abstractmethod
    def get_columns(self) -> List[str]:
        pass

    def to_dataframe(self):
        dataframe=pandas.DataFrame(columns = self.get_columns())
        dataframe = dataframe.append(
            [dataframes.asdict(entry) for entry in self.get_entries()]
        )
        return dataframe


    def write_csv(self, outfile):
        self.to_dataframe().write_csv(outfile, sep=CSV_SEP)

    @staticmethod
    def Dataframe_From_File(file, columns):
        return pandas.read_csv(file, sep=CSV_SEP, header=None, names=columns)
 # }}}

@dataclass
class SCSV_Entry(CSV_Entry): # {{{
    id: str
    functionality: str
    how_implemented: str
    path: List[str]
    category: str

    @staticmethod
    def From_Dataframe_Row(row):
        # print(f"{row['path']=}")
        print(str(row["path"]))
        return SCSV_Entry(
            id              = row["id"], 
            functionality   = row["functionality"],
            how_implemented = row["how_implemented"],
            path            = re.split(r"\s*[\\/]\s*", row["path"]),
            category        = row["category"]
        )
 # }}}


@dataclass
class MSCV_Entry(CSV_Entry): # {{{
    SEP_ids = "+"
    SEP_how_implemented = "+"
    SEP_paths = "+"
    SEP_categories = "+"
    SEP_pathelements = ' \ '
    
    functionality: str
    ids: List[str]
    how_implemented: List[str]
    paths: List[List[str]]
    categories: List[str]

    def write_functionality(self):
        return self.functionality;

    def write_ids(self):
        return MCSV_Entry.SEP_ids.join(self.ids)

    def write_how_implemented(self):
        return MCSV_Entry.SEP_how_implemented.join(self.how_implemented)

    def write_paths(self):
        return MCSV_Entry.SEP_paths.join(self.paths)

    def write_categories(self):
        return MCSV_Entry.SEP_categories.join([MCSV_Entry.SEP_pathelement.join(pathelements) for pathelement in self.paths])
 # }}}

@dataclass
class Merged_Functionality(): # {{{

    functionality: str
    scsv_entries: List[SCSV_Entry] = field(default_factory = list)

    def merge_with(self, scsv_entry):
        scsv_entries.append(scsv_entry)

    def to_MCSV(self):
        return MCSV_Entry(
            functionality   = self.functionality, 
            ids             = [entry.id for entry in self.scsv_entries], 
            how_implemented = [entry.how_implemented for entry in self.scsv_entries], 
            paths           = [entry.path for entry in self.scsv_entries], 
            categories      = [entry.category for entry in self.scsv_entries]
        )


 # }}}

@dataclass
class MCSV_Dataset(CSV_Dataset): # {{{

    rows: List[MSCV_Entry] = field(default_factory=list)

    COLUMNS = ["ids", "functionality", "how_implemented", "paths", "categories"]

    def get_entries():
        return rows

    def get_columns():
        return MCSV_Dataset.COLUMNS


 # }}}
@dataclass
class SCSV_Dataset(CSV_Dataset): # {{{
    COLUMNS = ["id", "functionality", "how_implemented", "path", "category"]

    entries: List[SCSV_Entry] = field(default_factory=list)

    def get_entries(self):
        return self.entries

    def get_columns():
        return SCSV_Dataset.COLUMNS
    
    @staticmethod
    def From_Dataframe(dataset):
        rows = [row for i,row in dataset.iterrows()]
        print(f"{rows[0]['functionality']=}")

        return SCSV_Dataset(entries = [SCSV_Entry.From_Dataframe_Row(row) for row in rows])

    @staticmethod
    def Dataframe_From_File(file):
        return CSV_Dataset.Dataframe_From_File(file, SCSV_Dataset.COLUMNS)
 # }}}

# end data spec }}}




@dataclass
class TransformRule: # {{{
    leftPattern: str
    funcReplacement: str
    prefix: str

    def IsDeletion(self):
        return funcReplacement == ""


    "returns None if the input is not of the correct form"
    @staticmethod
    def Parse(line):
        pat=r"^\s*(.*)\s+-->\s*([^;]*)(;.*)?"
        match = re.findall(pat, line)
        if match:
            groups=match[0]
            return TransformRule(groups[0], groups[1], groups[2])
        else:
            return None
 # }}}

@dataclass
class IniAssignment: # {{{
    key: str
    val: str

    @staticmethod
    def Parse(line):
        return None
 # }}}

def ParseMergeConfigFile(): # {{{
    result=[]
    with open(mergeConfigFile, "r") as fileIn:
        line = fileIn.readline()
        lineNo = 0
        commentLineRE = r"^\s*(#.*)?$"
        while line:
            lineNo = lineNo+1

            if re.match(commentLineRE, line): 
                line = fileIn.readline()
                continue

            line=line.strip()
            parsed = IniAssignment.Parse(line) or TransformRule.Parse(line)
            if parsed:
                result.append(parsed)
            else:
                print(f"Line #{lineNo} : {line} of {mergeConfigFile} could not be parsed", file=sys.stderr)
                # return None

            line = fileIn.readline()
 # }}}

