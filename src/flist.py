from __future__ import annotations
from abc import ABC, abstractmethod
import dataclasses;
from dataclasses import dataclass, field
import os
import re
import sys
import argparse
import pandas
from typing import List, Any, Dict
import pathlib;
from pathlib import Path
import flist_argtype as argtype
import flist_io as io

# ---- State that holds the multiple steps together. Must be completely inferrable by pointing to a workspace dir, and must also be optional

# ---- Data documentation stub:

# DCSV_CT2: CT2 dynamic csv-like data (different numbers of columns per line -> state based)
# SCSV: single csv -- all cells are atomar (no lists)
# MCSV: merged csv
# FinalForm: 

CSV_SEP = ";"


# CSV infrastructure

class CSV_Entry(ABC):
    """ this class is just a marker for future abstractions over CSV entries"""
    pass


# this abstract class controls serialization and deserialization of CSV datasets
class CSV_Dataset(ABC):
    """
    super class for any csv dataset in the flist project.
    CSV files in this schemes are not ever considered to have a "header" row; 
    this is because they are often read in in series, where single headers would be 
    a source of conflicts.
    """

    @abstractmethod
    def get_rows(self) -> List[CSV_Entry]:
        """
        returns a list of CSV_Entry. If the CSV_Entry instance is a dataclass,
        the string representation of its members and their names can automatically describe a CSV table
        """
        pass

    @abstractmethod
    def get_columns(self) -> List[str]:
        """
        return the columns of the CSV scheme
        """
        pass

    def to_dataframe(self):
        """
        automatically construct the dataframe for this CSV dataset
        """
        dataframe = pandas.DataFrame(columns=self.get_columns())
        for row in self.get_rows():
            dataframe = dataframe.append(row, ignore_index=True)
        return dataframe

    def write_csv(self, outfile):
        """
        This attempts to convert the CSV_Entry fields from self.get_rows to a pandas.DataFrame, 
        which is then written to a CSV file.
        """
        self.to_dataframe().to_csv(outfile, sep=CSV_SEP, index=False, header=False)
        io.msg(f"written CSV output to {outfile}")

    @staticmethod
    def Dataframe_From_File(file: Path, columns):
        """
        This attempts to convert a file to a dataframe, based on a list of column names given
        """
        if not file.exists():
            raise io.FlistException(f"nonexistent file path: {file}")
        return pandas.read_csv(file, sep=CSV_SEP, header=None, names=columns, keep_default_na=False)

    @staticmethod
    def Dataframe_From_Files(files, columns):
        """
        Based on a list of columns, return the dataframe that corresponds to the content of the given files
        """
        if len(files) == 0: raise io.FlistException("empty csv file list")
        for file in files:
            if not Path(file).exists():
                raise io.FlistException(f"file {file} does not exist")
        frames = [CSV_Dataset.Dataframe_From_File(file, columns) for file in files]
        return pandas.concat(frames)


# ---- Data structure

@dataclass
class SCSV_Entry(CSV_Entry):
    """
    represents a single line in a "SCSV" file. It represents a single row of data
    """
    id: str
    functionality: str
    how_implemented: str
    path: List[str]
    category: str

    @staticmethod
    def From_Dataframe_Row(row):
        # print(f"{row['path']=}")
        # print(str(row["id"]), str(row["path"]))
        return SCSV_Entry(
            id=row["id"],
            functionality=row["functionality"],
            how_implemented=row["how_implemented"],
            path=re.split(r"\s*[\\/]\s*", row["path"]),
            category=row["category"]
        )


@dataclass
class SCSV_Dataset(CSV_Dataset):
    """
    This class models the "single CSV" scheme of data. It is either provided
    by the CrypTool itself, or provided by another pipeline "step" of this project.
    The path elements (how to get to the functionality) are internally modeled as a list of path elements.
    """
    COLUMNS = ["id", "functionality", "how_implemented", "path", "category"]

    rows: List[SCSV_Entry] = field(default_factory=list)

    def get_rows(self):
        return [dataclasses.asdict(row) for row in self.rows]

    def get_columns(self):
        return SCSV_Dataset.COLUMNS

    def get_functionalities(self):
        functionalities = [row["functionality"] for row in self.get_rows()]
        uniqd = uniq(functionalities)
        # print(f"{functionalities=}")
        # print(f"{uniqd=}")
        return uniqd

    @staticmethod
    def From_Dataframe(dataset):
        rows = [row for i, row in dataset.iterrows()]

        return SCSV_Dataset(rows=[SCSV_Entry.From_Dataframe_Row(row) for row in rows])

    @staticmethod
    def Dataframe_From_File(file):
        return CSV_Dataset.Dataframe_From_File(file, SCSV_Dataset.COLUMNS)

    @staticmethod
    def Dataframe_From_Files(files):
        return CSV_Dataset.Dataframe_From_Files(files, SCSV_Dataset.COLUMNS)


@dataclass
class Merged_Functionality():
    functionality: str
    scsv_rows: List[SCSV_Entry] = field(default_factory=list)

    def merge_with(self, scsv_row):
        self.scsv_rows.append(scsv_row)

    def to_MCSV(self):
        return MCSV_Entry(
            functionality=self.functionality,
            ids=[row["id"] for row in self.scsv_rows],
            how_implemented=[row["how_implemented"] for row in self.scsv_rows],
            paths=[row["path"] for row in self.scsv_rows],
            categories=[row["category"] for row in self.scsv_rows]
        )


@dataclass
class MCSV_Entry(CSV_Entry):
    SEP_ids = "+"
    SEP_how_implemented = "\\"
    SEP_paths = " <br /> "
    SEP_categories = " <br \>"
    SEP_pathelement = " \\ "

    functionality: str
    ids: List[str]
    how_implemented: List[str]
    paths: List[List[str]]
    categories: List[str]

    @staticmethod
    def processStartOfPath(path):
        if path[0].startswith("JCT"):
            headReplacement = f"[{path[0][4:]}]"
            replaced = list(path)
            replaced[0] = headReplacement
            return replaced
        else:
            return path[1:]

    def filter_for_cryptoolstring(self, ctstring):
        return MCSV_Entry(

            functionality=self.functionality,
            ids=[element for element in self.ids if element.startswith(ctstring)],
            how_implemented=[element.replace(ctstring + ":", "") for element in self.how_implemented if
                             element.startswith(ctstring)],
            paths=[MCSV_Entry.processStartOfPath(element) for element in self.paths if element[0].startswith(ctstring)],
            categories=[element for element in self.categories]
        )

    def get_ids_for(self, ctstring):
        """
        ctstring: one of "CT1,CT2,CTO,JCT"
        """
        pass

    @staticmethod
    def merge_functionality(functionality):
        return functionality;

    @staticmethod
    def merge_ids(ids):
        uniqd = uniq(ids)
        appended = MCSV_Entry.SEP_ids.join(uniqd)
        if (ids != uniqd):
            raise io.FlistException(f"ids are not unique for {self}: {ids} != {uniqd}")
        return appended

    @staticmethod
    def merge_how_implemented(how_implemented):
        uniqd = uniq(how_implemented)
        appended = MCSV_Entry.SEP_how_implemented.join(uniqd)
        return appended

    @staticmethod
    def merge_paths(paths):
        uniqd = uniq(paths)
        appended = MCSV_Entry.SEP_paths.join([MCSV_Entry.SEP_pathelement.join(el) for el in uniqd])
        return appended

    @staticmethod
    def merge_categories(categories):
        uniqd = uniq(categories)
        appended = MCSV_Entry.SEP_categories.join(uniqd)
        return appended

    # TODO: unmerge: check that all cells have the same number of elements after unmerging?

    @staticmethod
    def unmerge_functionality(merged):
        return merged.strip()

    @staticmethod
    def unmerge_ids(merged):
        return merged.strip().split(MCSV_Entry.SEP_ids)

    @staticmethod
    def unmerge_how_implemented(merged):
        return merged.strip().split(MCSV_Entry.SEP_how_implemented)

    @staticmethod
    def unmerge_paths(merged):
        lvl1 = merged.strip().split(MCSV_Entry.SEP_paths)
        lvl2 = [pathelement.split(MCSV_Entry.SEP_pathelement) for pathelement in lvl1]
        return lvl2

    @staticmethod
    def unmerge_categories(merged):
        return merged.strip().split(MCSV_Entry.SEP_categories)

    def to_dataframe_row(self):
        # if len(uniq(self.categories)) > 1:
        #     print(f"{self.functionality} {self.ids}: {uniq(self.categories)}", file=sys.stderr)

        result = {
            "functionality": MCSV_Entry.merge_functionality(self.functionality),
            "ids": MCSV_Entry.merge_ids(self.ids),
            "how_implemented": MCSV_Entry.merge_how_implemented(self.how_implemented),
            "paths": MCSV_Entry.merge_paths(self.paths),
            "categories": MCSV_Entry.merge_categories(uniq(self.categories)[:1])
        }
        return result

    @staticmethod
    def From_Dataframe_Row(row):
        functionality_merged = row["functionality"]
        ids_merged = row["ids"]
        how_implemented_merged = row["how_implemented"]
        paths_merged = row["paths"]
        categories_merged = row["categories"]
        functionality = MCSV_Entry.unmerge_functionality(functionality_merged)
        ids = MCSV_Entry.unmerge_ids(ids_merged)
        how_implemented = MCSV_Entry.unmerge_how_implemented(how_implemented_merged)
        paths = MCSV_Entry.unmerge_paths(paths_merged)
        categories = MCSV_Entry.unmerge_categories(categories_merged)
        return MCSV_Entry(
            functionality=functionality,
            ids=ids,
            how_implemented=how_implemented,
            paths=paths,
            categories=categories
        )


@dataclass
class MCSV_Dataset(CSV_Dataset):
    rows: List[MCSV_Entry] = field(default_factory=list)

    COLUMNS = ["ids", "functionality", "how_implemented", "paths", "categories"]

    def get_rows(self):
        return [row.to_dataframe_row() for row in self.rows]

    def get_columns(self):
        return MCSV_Dataset.COLUMNS

    @staticmethod
    def From_Dataframe(dataframe):
        rows = [MCSV_Entry.From_Dataframe_Row(row) for i, row in dataframe.iterrows()]
        return MCSV_Dataset.From_Rows(rows)

    @staticmethod
    def From_Rows(rows: List[MCSV_Entry]):
        return MCSV_Dataset(rows)

    @staticmethod
    def Dataframe_From_File(file):
        return CSV_Dataset.Dataframe_From_File(file, MCSV_Dataset.COLUMNS)

    @staticmethod
    def Dataframe_From_Files(files):
        return CSV_Dataset.Dataframe_From_Files(files, MCSV_Dataset.COLUMNS)


@dataclass
class FinalForm_Entry:
    functionality: str
    how_implemented: Dict[str, str]
    paths: Dict[str, str]
    categories: str

    @staticmethod
    def From_MCSV(mcsv: MCSV_Entry):
        functionality = mcsv.functionality
        categories = MCSV_Entry.merge_categories(mcsv.categories)
        how_implemented = dict()
        paths = dict()
        for ctid in ["CT1", "CT2", "CTO", "JCT"]:
            filtered = mcsv.filter_for_cryptoolstring(ctid)
            how_implemented[ctid] = MCSV_Entry.merge_how_implemented(filtered.how_implemented)
            paths[ctid] = MCSV_Entry.merge_paths(filtered.paths)

        return FinalForm_Entry(functionality, how_implemented, paths, categories)

    @staticmethod
    def From_Dataframe_Row(row):
        functionality = row["functionality"]
        categories = row["categories"]
        how_implemented = dict()
        paths = dict()
        for ctid in ["CT1", "CT2", "CTO", "JCT"]:
            how_implemented[ctid] = row[f"how_implemented_{ctid}"]
            paths[ctid] = row[f"paths_{ctid}"]

        return FinalForm_Entry(functionality, how_implemented, paths, categories)

    def to_dataframe_row(self):
        result = {}
        result["functionality"] = self.functionality
        result["categories"] = self.categories
        for ctid in ["CT1", "CT2", "CTO", "JCT"]:
            column_HI = f"how_implemented_{ctid}"
            column_paths = f"paths_{ctid}"
            result[column_HI] = self.how_implemented[ctid]
            result[column_paths] = self.paths[ctid]

        return result


@dataclass
class FinalForm_Dataset(CSV_Dataset):
    COLUMNS = ["functionality",
               "how_implemented_CT1",
               "how_implemented_CT2",
               "how_implemented_JCT",
               "how_implemented_CTO",
               "paths_CT1",
               "paths_CT2",
               "paths_JCT",
               "paths_CTO",
               "categories"]
    rows: List[FinalForm_Entry] = field(default_factory=list)

    def get_rows(self):
        return [row.to_dataframe_row() for row in self.rows]

    def get_columns(self):
        return FinalForm_Dataset.COLUMNS

    @staticmethod
    def From_Dataframe(dataframe):
        rows = [FinalForm_Entry.From_Dataframe_Row(row) for i, row in dataframe.iterrows()]
        return FinalForm_Dataset.From_Rows(rows)

    @staticmethod
    def From_Rows(rows: List[MCSV_Entry]):
        return FinalForm_Dataset(rows)

    @staticmethod
    def From_MCSV(mcsv_set):
        return FinalForm_Dataset.From_Rows([FinalForm_Entry.From_MCSV(row) for row in mcsv_set.rows])

    @staticmethod
    def Dataframe_From_File(file):
        return CSV_Dataset.Dataframe_From_File(file, FinalForm_Dataset.COLUMNS)

    @staticmethod
    def Dataframe_From_Files(files):
        return CSV_Dataset.Dataframe_From_Files(files, FinalForm_Dataset.COLUMNS)


# ---- Id formation

import hashlib
def makeId(functionality_en:str, path:str, how_implemented:str):
    return hashlib.md5(f"{functionality_en}{path}{how_implemented}".encode()).hexdigest()[:8]

# ---- Transform csv utilities

@dataclass
class TransformRule:
    leftPattern: str
    funcReplacement: str
    prefix: str

    def IsDeletion(self):
        return funcReplacement == ""

    "returns None if the input is not of the correct form"

    @staticmethod
    def Parse(line):
        pat = r"^\s*(.*)\s+-->\s*([^;]*)(;.*)?"
        match = re.findall(pat, line)
        if match:
            groups = match[0]
            return TransformRule(groups[0], groups[1], groups[2])
        else:
            return None


@dataclass
class IniAssignment:
    key: str
    val: str

    @staticmethod
    def Parse(line):
        return None


def ParseMergeConfigFile():
    result = []
    with open(mergeConfigFile, "r") as fileIn:
        line = fileIn.readline()
        lineNo = 0
        commentLineRE = r"^\s*(#.*)?$"
        while line:
            lineNo = lineNo + 1

            if re.match(commentLineRE, line):
                line = fileIn.readline()
                continue

            line = line.strip()
            parsed = IniAssignment.Parse(line) or TransformRule.Parse(line)
            if parsed:
                result.append(parsed)
            else:
                print(f"Line #{lineNo} : {line} of {mergeConfigFile} could not be parsed", file=sys.stderr)
                # return None

            line = fileIn.readline()


# --- utilities

def uniq(lst):
    seen = set()
    result = list()
    for el in lst:
        if not tuple(el) in seen:
            result.append(el)
            seen.add(tuple(el))
    return result
