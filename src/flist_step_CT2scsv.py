#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype
import flist_config as config
import dataclasses; from dataclasses import dataclass, field
import typing

import flist_api as api; from flist_api import implicitly
import flist
import flist_io as io

def checkValidRecord(record: list, file: Path, line: int):
    """checks whether a record obtained from CT2 dynamic csv is valid"""
    if len(record[0]) == 0 or len(record[1]) == 0:
        raise io.FlistException(f"at line {line} in {file}, encountered invalid CT2 csv output record.")


def appendToDF(entry: flist.SCSV_Entry):
    return df.append([entry.to_dataframe_dictionary()])

@dataclass
class LineparseRecord:
    input: Path = None
    state_which: str = ""
    state_currentfunc: list = field(default_factory=list)

    def __post_init__(self):
        self.state_currentfunc = ["", []]

    def parse(self, line: str, currentLine: int) -> typing.Optional[flist.SCSV_Entry]:

        # an empty line: marks that a functionality record is complete. it is finalized and returned in this if-branch.
        if len(line.strip()) == 0:
            self.state_which = "separator"
            checkValidRecord(self.state_currentfunc, input, currentLine)

            headerSplit = self.state_currentfunc[0].split(";")
            entriesSplit = [(entry.split(";"),lineNr) for (entry,lineNr) in self.state_currentfunc[1]]
            if(len(headerSplit) != 3):
                raise io.FlistException(f"at line {line} in {self.input}, encountered invalid csv output record.")
            functionality = headerSplit[0]
            # how_implemented = headerSplit[1].split("/")
            for (entrySplit,lineNr) in entriesSplit:
                if(len(entrySplit) != 3):
                    raise io.FlistException(f"at line {line} in {self.input}, encountered invalid csv output record.")
                how_implemented = entrySplit[1][1]
                path = entrySplit[2]
                category = ""
                id = "<no_id_-_dynamic_output>"
                df_row_dict = {
                    "functionality" : functionality,
                    "id" : id, 
                    "how_implemented" : how_implemented, 
                    "path" : path, 
                    "category" : category
                }
                # print(f"dbg: {how_implemented} | {path}")
                return flist.SCSV_Entry.From_Dataframe_Row(df_row_dict)

            self.state_currentfunc = ["", []]

        # a line that starts with a semicolon marks a single-path entry, which is added to the state array
        elif line.startswith(";"):
            self.state_which = "entry"
            self.state_currentfunc[1].append((line,currentLine))
            return None

        # non-empty non-semicolon-prefixed lines mark the header of a functionality record
        else:
            self.state_which = "header"
            self.state_currentfunc[0] = line
            return None


def reference_file_lockstep_exception(currentLine, id_reference, input) -> io.FlistException:
    return io.FlistException(f"while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: number of lines mismatches. This is probably an error in the correspondence between outputs of different languages of that tool.")

def reference_file_filelength_exception(currentLine, id_reference, input):
    return io.FlistException("while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: number of lines mismatches. This is probably an error in the correspondence between outputs of different languages of that tool.")

def reference_file_linecontent_exception(currentLine, id_reference, input):
    return io.FlistException("while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: lines do mismatch (one is empty, the other is not). This is probably an error in the correspondence between outputs of different languages of that CrypTool.")

def CreateCT2SCSV(input: Path, output: Path, id_reference: Path, toolname: str):
    resultDataset = flist.SCSV_Dataset()
    if not input.is_file():
        raise io.FlistException(f"{input=} does not exist")
    lines = []
    reference_lines = []

    # reading in both files

    with open(id_reference, "r") as opened:
        while line := opened.readline():
            reference_lines.append(line)
    with open(input, "r") as opened:
        while line := opened.readline():
            lines.append(line)


    # implicitly("prog.logger").info(f"{(input,output,id_reference,toolname)}")
    # sanity checks for checking wether the files match superficially

    if(len(lines) != len(reference_lines)):
        raise reference_file_filelength_exception(currentLine, id_reference, input)

    currentLine = 0
    for line in lines:
        reference_line = reference_lines[currentLine]

        currentLine += 1
        if len(reference_line.strip()) == 0 and len(line.strip()) != 0 or len(reference_line.strip()) != 0 and len(line.strip()) == 0 :
            raise reference_file_linecontent_exception(currentLine, id_reference, input)

    # parsing

    currentLine = 0
    currentRecord = LineparseRecord(input=input)
    currentRefRecord = LineparseRecord(input=id_reference)
    for line in lines:
        line = line.strip()
        reference_line = reference_lines[currentLine]
        reference_line = reference_line.strip()
        currentLine += 1

        currentResult = currentRecord.parse(line, currentLine)
        refResult = currentRefRecord.parse(reference_line, currentLine)
        if (currentResult and not refResult) or (not currentResult and refResult):
            raise reference_file_lockstep_exception(currentLine, id_reference, input)

        if currentResult:
            # prefix some fields with tool-specific info to match SCSV format (for legacy reasons)
            currentResult.category = flist.SCSV_Entry.dynamic_category_notset()
            currentResult.how_implemented = f"{toolname}:{currentResult.how_implemented}"
            currentResult.path.insert(0, currentResult.how_implemented)
            refResult.category = "<does_not_contain_category>"
            refResult.how_implemented = f"{toolname}:{refResult.how_implemented}"
            refResult.path.insert(0, refResult.how_implemented)

            # set id from id-reference result

            # print(f"dbg: inferring {refResult}")
            refResult.infer_id_from_fields(toolname)
            currentResult.id = refResult.id

            # prepare for next record
            resultDataset.rows.append(currentResult)
            currentRecord = LineparseRecord(input=input)
            currentRefRecord = LineparseRecord(input=id_reference)

    resultDataset.write_csv(output)

