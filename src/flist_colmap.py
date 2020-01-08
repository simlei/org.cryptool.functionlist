import sys
import os

import pandas
import datetime

import argparse; from argparse import FileType
import pathlib ; from pathlib  import Path
import flist_argtype as argtype

import dataclasses; from dataclasses import dataclass
import typing; from typing import List, Dict, Any

import flist
import flist_io as io
import flist_api as api; from flist_api import implicitly

import benedict; from benedict import benedict as bdict

def get_translations_file():
    return implicitly("workspace").path / "data" / "categories.csv"

def translate(translation_df: pandas.DataFrame, lang: str, category_en: str):
    for i,row in translation_df.iterrows():
        if row["en"] == category_en:
            return row[lang]
    raise io.FlistException(f"could not determine correct translation for category {category_en}; check that all categories in raw input files and all dynamically-attributed categories are maintained in the file {get_translations_file()}")

def map_category(catmapping_df: pandas.DataFrame, id: str):
    # if "dd12" in id: implicitly("prog.logger").info(f"queried for {id}")
    for i,row in catmapping_df.iterrows():
        if row["id"] == id:
            # if "dd12" in id: implicitly("prog.logger").info(f"matched {id} with {row['category']}")
            return row["category"]
    return None

blank_placeholder = "<enter category here>"
blank_disappears  = "<>"

def Add_Categories(colname: str, translationfile: Path, input: Path, mapfile: Path, language: str, feedbackfile: Path, output: Path):
    if not input.is_file():
        raise io.FlistException(f"file {input} does not exist")
    if not mapfile.is_file():
        raise io.FlistException(f"file {mapfile} does not exist")

    translations = pandas.read_csv(get_translations_file(), sep=";")
    feedbackfile_static = Path(__file__).parent.parent / "ws-static" / feedbackfile.relative_to( implicitly("workspace").path )

    dataset = flist.SCSV_Dataset.From_Dataframe(flist.SCSV_Dataset.Dataframe_From_Files([input]))

    catmapping_all = pandas.DataFrame(columns = ["id", "category"])

    df_cats_input = pandas.read_csv(mapfile, names=["id", "category", "path"], header=None, sep=";")
    df_cats_input.fillna('', inplace=True)
    df_cats_input = df_cats_input[
        (~ df_cats_input["id"].str.contains(blank_disappears)) & (~ df_cats_input["category"].str.contains(blank_placeholder))
    ]

    df_cats_feedback = pandas.DataFrame(columns = ["id", "category", "path"])
    if feedbackfile.is_file():
        df_cats_feedback = pandas.read_csv(feedbackfile, names=["id", "category", "path"], header=None, sep=";")
        df_cats_feedback.fillna('', inplace=True)
        df_cats_feedback = df_cats_feedback[
            (~ (df_cats_feedback["id"].str.contains(blank_disappears))) & (~ (df_cats_feedback["category"].str.contains(blank_placeholder)))
        ]
        implicitly("prog.logger").debug(f"==== Feedback cat file file ===")
        implicitly("prog.logger").debug(df_cats_feedback.to_string())
        # implicitly("prog.logger").debug(df_cats_feedback.to_string())
        # print(df_cats_input.to_string())


    df_writeback_input = pandas.DataFrame(columns = ["id", "category", "path"])
    df_writeback_feedback = pandas.DataFrame(columns = ["id", "category", "path"])
    df_writeback_feedback_matched = pandas.DataFrame(columns = ["id", "category", "path"])
    df_writeback_feedback_missing = pandas.DataFrame(columns = ["id", "category", "path"])


    has_unmatched_categories = False
    implicitly("prog.logger").debug(f"{feedbackfile=}")
    catFromFeedbackCounter = 0
    catFromInputFileCounter = 0

    # print(df_cats_input.to_string())
    for entry in dataset.rows:
        id = entry.id
        category = entry.category
        if category != flist.SCSV_Entry.dynamic_category_notset(): # TODO: configurable?
            raise FlistException(f"SCSV file {input} is being assigned categories dynamically, but has category {category} which is not the 'needs category assignment' placeholder that was expected")

        category_from_input = map_category(df_cats_input, id)
        category_from_feedback = map_category(df_cats_feedback, id)
        implicitly("prog.logger").debug(f"getting cat for {id}")
        implicitly("prog.logger").debug(f"{category_from_input=}, {category_from_feedback=}")

        if category_from_input:
            df_writeback_input = df_writeback_input.append([{"id":entry.id, "category":category_from_input}])
            catFromInputFileCounter += 1
        elif category_from_feedback:
            df_writeback_feedback_matched = df_writeback_feedback_matched.append([{"id": entry.id, "category": category_from_feedback, "path": entry.to_dataframe_dictionary()["path"]}])
            catFromFeedbackCounter += 1

        if category_from_input or category_from_feedback:
            mapped_cat = category_from_input or category_from_feedback
            translated_mapped_cat = translate(translations, language, mapped_cat)
            entry.category = translated_mapped_cat
        else:
            df_writeback_feedback_missing = df_writeback_feedback_missing.append([{"id": entry.id, "category": blank_placeholder, "path": entry.to_dataframe_dictionary()["path"]}])
            has_unmatched_categories = True

    df_writeback_feedback = df_writeback_feedback.append(df_writeback_feedback_matched)
    df_writeback_feedback = df_writeback_feedback.append(df_writeback_feedback_missing)
    implicitly("prog.logger").info(f"{catFromInputFileCounter} of {len(dataset.rows)} entries have been assigned categories based on their ids in {input}")
    implicitly("prog.logger").info(f"{catFromFeedbackCounter} of {len(dataset.rows)} entries have been assigned categories based on their ids in {feedbackfile}")
    if catFromFeedbackCounter > 0:
        implicitly("prog.logger").info(f"[ NOTE ] when running the program with --initws, the file {feedbackfile} will be overwritten by the prototypical workspace and the manual entries may be lost. Consider merging them with the corresponding file of {input} in ./ws-static!")

    if has_unmatched_categories:
        api.implicitly("prog.logger").warning(f"[[ WARNING ]] : {len(df_writeback_feedback_missing)} entries in {input} could not be assigned categories. To remedy this, edit the categories manually in {feedbackfile}")


    # implicitly("prog.logger").info(f"writing feedbackfile with ids to {feedbackfile} with ids: {df_writeback_feedback['id'].tolist()}")
    df_writeback_feedback.to_csv(feedbackfile, sep=flist.CSV_SEP, index=False, header=False)
    dataset.write_csv(output)
