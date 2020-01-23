#!/usr/bin/env python3

import flist

import re
import sys
import fileinput
import argparse
import flist
import dataclasses; from dataclasses import dataclass, field
from pathlib import Path
import flist_argtype as argtype
import typing; from typing import List, Any
import flist_io as io
import flist_api as api; from flist_api import implicitly

# reads a file, and substitutes patterns in it.
# patterns are marked in the file as ${key}
def substituteFileToFile(infilePath, outfilePath, **kwargs):
    if not Path(infilePath).exists():
        raise io.FlistException(f"{infilePath=} does not exist")
    if Path(infilePath).resolve().absolute() == Path(outfilePath).resolve().absolute():
        raise io.FlistException(f"no in-place substitution allowed -- {infilePath=} is the same as the output path")
    with open(outfilePath, "w") as outfile:
        with open(infilePath, "r") as infile:
            while replaced := infile.readline():
                for k,v in kwargs.items():
                    replaced = replaced.replace("${"+k+"}", v)
                print(replaced, end='', file=outfile)

def substituteFileToStr(infilePath, **kwargs):
    if not Path(infilePath).exists():
        raise io.FlistException(f"{infilePath=} does not exist")
    builder = ""
    with open(infilePath, "r") as infile:
        while replaced := infile.readline():
            for k,v in kwargs.items():
                # if k == "odd_even":
                #     print(f"orig: {replaced}")
                replaced = replaced.replace("${"+k+"}", v)
                # if k == "odd_even":
                #     print(f"replaced with {v=}: {replaced}")
            builder = builder + replaced
    return builder

def getFileContent(path):
    if not Path(path).is_file:
        raise io.FlistException(f"not a file: {path}")
    with open(path, "r") as opened:
        return "".join(opened.readlines())


def MakeHTML(input: Path, output: Path, template_html: Path):
    outputFile = output
    dataframe = flist.FinalForm_Dataset.Dataframe_From_Files([input])
    dataset = flist.FinalForm_Dataset.From_Dataframe(dataframe)
    categorytags=generate_category_tags(dataset, template_html)
    rowtags=generate_row_tags(dataset, template_html)
    interactive_html=generate_interactive(rowtags, categorytags, template_html)
    generate_index(interactive_html, outputFile, template_html)

def generate_interactive(rows, categories, template_html):
        return substituteFileToStr(template_html / "template_interactive.html",
                                   rows=rows,
                                   categories=categories
                                   )
def generate_index(interactive_html, target, template_html):
        implicitly("prog.logger").info(f"generating {target} from {template_html}")
        return substituteFileToFile(template_html / "template_index.html", target,
                                   interactive_part=interactive_html
                                   )

def generate_category_tags(dataset, template_html):
    all_categories = []
    for row in dataset.rows:
        cat = row.categories
        if not cat.strip() in all_categories and cat.strip() and not "does_not_contain_category" in cat:
            all_categories.append(cat.strip())
    tags=""
    result=""
    for cat in all_categories:
        result += substituteFileToStr(template_html / "fragment_category.html", 
                          categoryVal=cat,
                          categoryBody=re.sub(r"^\s*\d+\)\s*", "", cat)
                          )
    return result


def generate_row_tags(dataset, template_html: Path):
    result = ""
    odd="even"
    for row in dataset.rows:
        if odd == "odd":
            odd = "even"
        else:
            odd = "odd"
        result += substituteFileToStr(template_html / "fragment_row.html", 
                                   odd_even=odd,
                                   functionality=row.functionality,
                                   how_implemented_CT1=row.how_implemented["CT1"],
                                   how_implemented_CT2=row.how_implemented["CT2"],
                                   how_implemented_CTO=row.how_implemented["CTO"],
                                   how_implemented_JCT=row.how_implemented["JCT"],
                                   paths_CT1=row.paths["CT1"],
                                   paths_CT2=row.paths["CT2"],
                                   paths_CTO=row.paths["CTO"],
                                   paths_JCT=row.paths["JCT"],
                                   category=row.categories
                                   )

    return result

