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

    catmapping_all = pandas.DataFrame(columns = ["id", "category"])

    df_cats_input = pandas.read_csv(catfile, names=["id", "category"], header=None, sep=";")
    df_cats_input.fillna('', inplace=True)
    df_cats_input = df_cats_input[
        (~ df_cats_input["id"].str.contains(blank_disappears)) & (~ df_cats_input["category"].str.contains(blank_placeholder))
    ]

    df_cats_feedback = None
    if feedbackfile.is_file():
        df_cats_feedback = pandas.read_csv(feedbackfile, names=["id", "category"], header=None, sep=";")
        df_cats_feedback.fillna('', inplace=True)
        df_cats_feedback = df_cats_feedback[
            (~ (df_cats_feedback["id"].str.contains(blank_disappears))) & (~ (df_cats_feedback["category"].str.contains(blank_placeholder)))
        ]
        # implicitly("prog.logger").debug(df_cats_feedback.to_string())
        # print(df_cats_input.to_string())


    df_writeback_input = pandas.DataFrame(columns = ["id", "category"])
    df_writeback_feedback = pandas.DataFrame(columns = ["id", "category", "path"])

    has_unmatched_categories = False
    for entry in dataset.rows:
        id = entry.id
        category = entry.category
        if category != flist.SCSV_Entry.dynamic_category_notset():
            raise FlistException(f"SCSV file {input} is being assigned categories dynamically, but has category {category} which is not the 'needs category assignment' placeholder that was expected")

        category_from_input = map_category(df_cats_input, category)
        category_from_feedback = map_category(df_cats_input, category)
        if category_from_input:
            df_writeback_input.append([{"id":entry.id, "category":category_from_input}])
        elif category_from_feedback:
            df_writeback_feedback.append([{"id": entry.id, "category": category_from_feedback, "path": entry.to_dataframe_dictionary()["path"]}])

        if category_from_input or category_from_feedback:
            mapped_cat = category_from_input or category_from_feedback
            translated_mapped_cat = translate(translations, language, mapped_cat)
            entry.category = translated_mapped_cat
        else:
            df_writeback_feedback.append([{"id": entry.id, "category": blank_placeholder, "path": entry.to_dataframe_dictionary()["path"]}])
            has_unmatched_categories = True



    if has_unmatched_categories:
        api.implicitly("prog.logger").warning(f"[[ WARNING ]] : some entries in {input} could not be assigned categories. To remedy this, edit the categories manually in {feedbackfile}")


    df_writeback_feedback.to_csv(feedbackfile, sep=flist.CSV_SEP, index=False, header=False)
    dataset.write_csv(output)
