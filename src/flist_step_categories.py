import sys
import os

import pandas
import datetime

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

def get_category_file():
    return implicitly("workspace").path / "categories.csv"


def translate(translation_df: pandas.DataFrame, lang: str, category_en: str):
    for i,row in translation_df.iterrows():
        if row["en"] == category_en:
            return row[lang]
    raise io.FlistException(f"could not determine correct translation for category {category_en}; check that all categories in raw input files and all dynamically-attributed categories are maintained in the file {get_category_file()}")

def map_category(catmapping_df: pandas.DataFrame, id: str):
    for i,row in catmapping_df.iterrows():
        if row["id"] == id:
            return row["category"]
    return None

blank_placeholder = "<enter category here>"
blank_disappears  = "<>"

def Add_Categories(input: Path, catfile: Path, language: str, feedbackfile: Path, output: Path):
    if not input.is_file():
        raise io.FlistException("file {input} does not exist")
    if not catfile.is_file():
        raise io.FlistException("file {catfile} does not exist")

    translations = pandas.read_csv(get_category_file(), names=["en", "de"], header=None, sep=";")
    feedbackfile_static = Path(__file__).parent.parent / "ws-static" / feedbackfile.relative_to( implicitly("workspace").path )

    dataset = flist.SCSV_Dataset.From_Dataframe(flist.SCSV_Dataset.Dataframe_From_Files([input]))
    catmapping_df = pandas.read_csv(catfile, names=["id", "category"], header=None, sep=";")
    catmapping_df.fillna('', inplace=True)

    cats_user = None
    if feedbackfile.is_file():
        cats_user = pandas.read_csv(feedbackfile, names=["id", "category"], header=None, sep=";")
        cats_user.fillna('', inplace=True)

        cats_user = cats_user[
            (~ (cats_user["id"].str.contains(blank_disappears))) & (~ (cats_user["category"].str.contains(blank_placeholder)))
        ]
        catmapping_df = catmapping_df.append(cats_user)
        implicitly("prog.logger").debug(cats_user.to_string())
        # print(catmapping_df.to_string())

    catmapping_df = catmapping_df[
        (~ catmapping_df["id"].str.contains(blank_disappears)) & (~ catmapping_df["category"].str.contains(blank_placeholder))
    ]
    # print(catmapping_df.to_string())

    ids_with_no_category_mapping = []

    for entry in dataset.rows:
        id = entry.id
        category = entry.category
        if category != flist.SCSV_Entry.dynamic_category_notset():
            raise FlistException(f"SCSV file {input} is being assigned categories dynamically, but has category {category} which is not the 'needs category assignment' placeholder that was expected")

        category_from_mapping = map_category(catmapping_df, category)
        if not category_from_mapping:
            ids_with_no_category_mapping.append(entry)
            entry.category = flist.SCSV_Entry.dynamic_category_placeholder()
        else:
            translated_mapped_cat = translate(translations, language, category_from_mapping)
            entry.category = translated_mapped_cat


    # writeback modality of category mappings:
    # - per file
    #   - mapping not successfully applied -> throw out
    #   - mapping successfully applied     -> keep
    # - but how to avoid deleting stuff accidentally - if e.g. one CrypTool was omitted in processing?
    # - clean solution: 
    #   - apply make a "diff file" for which the user can decide if it's applied to the template
    # - all mappings that were provided
    # - including: all mappings that were applied successfully
    # - minus, the entries that could not be applied successfully
    # 
    # 

    if len(ids_with_no_category_mapping) > 0:

        existing_manual_lines = []
        
        # if there are ids that are not 
        cats_user_writeback = cats_user[
            (~ cats_user["id"].isin(ids_with_)) & (~ cats_user["category"].str.contains(blank_placeholder))
        ]

        # if feedbackfile.is_file():
        #     with open(feedbackfile, "r") as opened:
        #         while (line := opened.readline()):
        #             existing_manual_lines.append(line.strip())

        writeback_manual_lines = [line for line in existing_manual_lines if not blank_disappears in line]
        for id in [e.id for e in ids_with_no_category_mapping]:
            writeback_manual_lines = [line for line in writeback_manual_lines if not id in line]

        for entry in ids_with_no_category_mapping:
            writeback_manual_lines.append(f"{entry.id};{blank_placeholder};{entry.to_dataframe_dictionary()['path']}")

        with open(feedbackfile_static, "w") as opened:
            opened.write(f"{blank_disappears};\n")
            opened.write(f"{blank_disappears}*added {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*;\n")
            opened.write(f"{blank_disappears};\n")
            opened.write("\n".join(writeback_manual_lines))

        api.implicitly("prog.logger").warning(f"[[ WARNING ]] : some entries in {input} could not be assigned categories. To remedy this, edit the categories manually in {writeback_manual_lines}")

    dataset.write_csv(output)
    # with open(input, "") as opened
