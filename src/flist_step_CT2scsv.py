#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype
import flist_config as config
import dataclasses; from dataclasses import dataclass, field

import flist
import flist_io as io

def checkValidRecord(record: list, file: Path, line: int):
    """checks whether a record obtained from CT2 dynamic csv is valid"""
    if len(record[0]) == 0 or len(record[1]) == 0:
        raise io.FlistException(f"at line {line} in {file}, encountered invalid CT2 csv output record.")


@dataclass 
class ParsedEntry:
    functionality: str
    id: str
    path: str
    how_implemented: str
    category: str

    def appendToDF(self, df: pandas.DataFrame):
        record_dict = {
            "functionality" : self.functionality,
            "id" : self.id,
            "how_implemented": self.how_implemented, 
            "path" : self.path,
            "category" : self.category
        }
        return df.append([record_dict])

@dataclass
class LineparseRecord:
    input: Path = None
    state_which: str = ""
    state_currentfunc: list = field(default_factory=list)

    def __post_init__(self):
        self.state_currentfunc = ["", []]

    def parse(self, line: str, currentLine: int):
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
                howimpl_payload = entrySplit[1][1]
                how_implemented = f"CT2:{howimpl_payload}"
                pathelements = entrySplit[2].split("\\ ")
                path = " \\ ".join([how_implemented] + pathelements)
                category = "0) TODO: not inferred for dynamic CT2 output"
                id = f"CT2:dynamic:{flist.makeId(functionality, path, howimpl_payload)}"
                record_dict = {
                    "functionality" : functionality,
                    "id" : id, 
                    "how_implemented" : how_implemented, 
                    "path" : path, 
                    "category" : category
                }
                result = ParsedEntry(**record_dict)
                return result

            self.state_currentfunc = ["", []]
        elif line.startswith(";"):
            self.state_which = "entry"
            self.state_currentfunc[1].append((line,currentLine))
            return None
        else:
            self.state_which = "header"
            self.state_currentfunc[0] = line
            return None

def CreateCT2SCSV(input: Path, output: Path, id_reference: Path):
    dataframe = pandas.DataFrame(columns=flist.SCSV_Dataset.COLUMNS)
    if not input.is_file():
        raise io.FlistException(f"{input=} does not exist")
    currentLine = 0
    lines = []
    reference_lines = []
    with open(id_reference, "r") as opened:
        while line := opened.readline():
            reference_lines.append(line)
    with open(input, "r") as opened:
        while line := opened.readline():
            lines.append(line)

    if(len(lines) != len(reference_lines)):
        raise io.FlistException("while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: number of lines mismatches. This is probably an error in the correspondence between outputs of different languages of that tool.")
    for line in lines:
        reference_line = reference_lines[currentLine]

        currentLine += 1
        if len(reference_line.strip()) == 0 and len(line.strip()) != 0 or len(reference_line.strip()) != 0 and len(line.strip()) == 0 :
            raise io.FlistException("while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: lines do mismatch (one is empty, the other is not). This is probably an error in the correspondence between outputs of different languages of that CrypTool.")

    currentLine = 0
    currentRecord = LineparseRecord(input=input)
    currentRefRecord = LineparseRecord(input=id_reference)
    for line in lines:
        line = line.strip()
        reference_line = reference_lines[currentLine]
        currentLine += 1

        currentResult = currentRecord.parse(line, currentLine)
        refResult = currentRefRecord.parse(reference_line, currentLine)
        if (currentResult and not refResult) or (not currentResult and refResult):
            raise io.FlistException("while extracting reference ids from line {currentLine} in {id_reference} for csv file {input}: parsing did not happen in lockstep. This is probably an error in the correspondence between outputs of different languages of that CrypTool.")

        if currentResult:
            currentResult.id = refResult.id
            currentResult.appendToDF(dataframe)

    dataframe.to_csv(output, sep=flist.CSV_SEP, index=False, header=False)

