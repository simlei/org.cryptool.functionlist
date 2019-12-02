#!/usr/bin/env python3

import sys
import os

import pandas

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype
import flist_config as config

import flist
import flist_io as io

def checkValidRecord(record: list, file: Path, line: int):
    """checks whether a record obtained from CT2 dynamic csv is valid"""
    if len(record[0]) == 0 or len(record[1]) == 0:
        raise io.FlistException(f"at line {line} in {file}, encountered invalid CT2 csv output record.")

def appendRecord(df: pandas.DataFrame, currentFrame: list, inputfile: Path, currentLine: int):
    """
    appends a record (obtained from CT2 dynamic csv) to a dataframe and returns it.
    assigns ids for rows based on the line number and prefixes with 'CT2:dynamic'
    """
    headerSplit = currentFrame[0].split(";")
    entriesSplit = [(entry.split(";"),lineNr) for (entry,lineNr) in currentFrame[1]]
    result = df
    if(len(headerSplit) != 3):
        raise io.FlistException(f"at line {line} in {inputfile}, encountered invalid CT2 csv output record.")
    functionality = headerSplit[0]
    # how_implemented = headerSplit[1].split("/")
    for (entrySplit,lineNr) in entriesSplit:
        if(len(entrySplit) != 3):
            raise io.FlistException(f"at line {line} in {inputfile}, encountered invalid CT2 csv output record.")
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
        result = result.append([record_dict])
    return result

def CreateCT2SCSV(inputfile: Path, outputfile: Path):
    dataframe = pandas.DataFrame(columns=flist.SCSV_Dataset.COLUMNS)
    if not inputfile.is_file():
        raise io.FlistException(f"{inputfile=} does not exist")
    state_which = ""
    state_currentfunc = ["", []]
    currentLine = 0
    with open(inputfile, "r") as input:
        while line := input.readline():
            line = line.strip()
            currentLine += 1
            if len(line.strip()) == 0:
                state_which = "separator"
                checkValidRecord(state_currentfunc, inputfile, currentLine)
                dataframe = appendRecord(dataframe, state_currentfunc, inputfile, currentLine)
                state_currentfunc = ["", []]
            elif line.startswith(";"):
                state_which = "entry"
                state_currentfunc[1].append((line,currentLine))
            else:
                state_which = "header"
                state_currentfunc[0] = line
        try:
            checkValidRecord(state_currentfunc, inputfile, currentLine)
            dataframe = appendRecord(dataframe, state_currentfunc)
        except:
            pass
    dataframe.to_csv(outputfile, sep=flist.CSV_SEP, index=False, header=False)

def argparse_contribute(parser, state: config.FlistProgramState):
    parser.add_argument(
        "input", 
        type=argtype.FilePathExisting, 
        nargs="?", 
        default=state.defaults.ct2scsv.input
    )
    parser.add_argument("--output", 
                        type=argtype.FilePath, 
                        default=state.defaults.ct2scsv.output
                        )

if __name__ == "__main__":
    parsed, flist_state = config.parse_args(sys.argv[1:], argparse_contribute)

    try:
        CreateCT2SCSV(parsed.input, parsed.output)
    except io.FlistException as e:
        io.err(str(e), e)
        exit(1)
