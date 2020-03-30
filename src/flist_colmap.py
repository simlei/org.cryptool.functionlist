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

import csv

def translate(translationfile: Path, translation_df: pandas.DataFrame, lang: str, category_en: str) -> typing.Optional[str]:
    for i,row in translation_df.iterrows():
        if row["en"] == category_en:
            return row[lang]
    return None

def id_diff_and_map_column(colname: str, catmapping_df: pandas.DataFrame, id: str, entry: flist.SCSV_Entry) -> typing.Optional[str]:
    outputfile = "/home/simon/sandbox/featurelist/ct_functionlist/idmap.txt"
    __id = entry.id
    entry.infer_id_from_fields(id[0:3], flist.makeId_OLD)
    oldid = entry.id
    entry.infer_id_from_fields(id[0:3], flist.makeId_NEW)
    newid  = entry.id
    entry.id = __id
    with open(outputfile, "a") as out:
        out.writelines([ f"{oldid} {newid}" ])
        print(f"{oldid} {newid}\n")
    for i,row in catmapping_df.iterrows():
        if row["id"] == id:
            return row[colname]
    return None

def map_column(colname: str, catmapping_df: pandas.DataFrame, id: str):
    # if "dd12" in id: implicitly("prog.logger").info(f"queried for {id}")
    for i,row in catmapping_df.iterrows():
        if row["id"] == id:
            return row[colname]
    return None

blank_placeholder = "<enter value here>"
blank_disappears  = "<>"



def Dispatch_Map_Columns(colname: str, translationfile: Path, input: Path, mapfile: Path, language: str, feedbackfile: Path, output: Path, id_diff=False):
    Map_Columns(colname, translationfile, input, mapfile, language, feedbackfile, output, os.environ.get("FLIST_IDMAP") or id_diff)

def Map_Columns(colname: str, translationfile: Path, input: Path, mapfile: Path, language: str, feedbackfile: Path, output: Path, id_diff=False):
    if not input.is_file():
        raise io.FlistException(f"file {input} does not exist")
    if not mapfile.is_file():
        raise io.FlistException(f"file {mapfile} does not exist")

    translations = pandas.read_csv(translationfile, quoting=csv.QUOTE_NONE, sep=";")
    feedbackfile_static = Path(__file__).parent.parent / "ws-static" / feedbackfile.relative_to( implicitly("workspace").path )

    dataset = flist.SCSV_Dataset.From_Dataframe(flist.SCSV_Dataset.Dataframe_From_Files([input]))

    catmapping_all = pandas.DataFrame(columns = ["id", colname])

    df_cats_input = pandas.read_csv(mapfile, quoting=csv.QUOTE_NONE, names=["id", colname, "path"], header=None, sep=";")
    df_cats_input.fillna('', inplace=True)
    df_cats_input = df_cats_input[
        (~ df_cats_input["id"].str.contains(blank_disappears)) & (~ df_cats_input[colname].str.contains(blank_placeholder))
    ]

    df_cats_feedback = pandas.DataFrame(columns = ["id", colname, "path"])
    if feedbackfile.is_file():
        df_cats_feedback = pandas.read_csv(feedbackfile, quoting=csv.QUOTE_NONE, names=["id", colname, "path"], header=None, sep=";")
        df_cats_feedback.fillna('', inplace=True)
        df_cats_feedback = df_cats_feedback[
            (~ (df_cats_feedback["id"].str.contains(blank_disappears))) & (~ (df_cats_feedback[colname].str.contains(blank_placeholder)))
        ]
        implicitly("prog.logger").debug(f"==== Feedback cat file file ===")
        implicitly("prog.logger").debug(df_cats_feedback.to_string())
        # implicitly("prog.logger").debug(df_cats_feedback.to_string())
        # print(df_cats_input.to_string())


    df_writeback_input = pandas.DataFrame(columns = ["id", colname, "path"])
    df_writeback_feedback = pandas.DataFrame(columns = ["id", colname, "path"])
    df_writeback_feedback_matched = pandas.DataFrame(columns = ["id", colname, "path"])
    df_writeback_feedback_missing = pandas.DataFrame(columns = ["id", colname, "path"])


    has_unmatched_categories = False
    implicitly("prog.logger").debug(f"{feedbackfile=}")
    catFromFeedbackCounter = 0
    catFromInputFileCounter = 0
    untranslatedCounter = 0

    # print(df_cats_input.to_string())
    for entry in dataset.rows:
        id = entry.id
        category = entry.category
        # if category != flist.SCSV_Entry.dynamic_category_notset(): # TODO: configurable?
        #     raise io.FlistException(f"SCSV file {input} is being assigned categories dynamically, but has {colname} {category} which is not the 'needs {colname} assignment' placeholder that was expected")

        category_from_input = map_column(colname, df_cats_input, id)
        category_from_feedback = map_column(colname, df_cats_feedback, id)
        if id_diff:
            id_diff_and_map_column(colname, df_cats_feedback, id, entry)
        implicitly("prog.logger").debug(f"getting cat for {id}")
        implicitly("prog.logger").debug(f"{category_from_input=}, {category_from_feedback=}")

        if category_from_input:
            df_writeback_input = df_writeback_input.append([{"id":entry.id, colname:category_from_input}])
            catFromInputFileCounter += 1
        elif category_from_feedback:
            df_writeback_feedback_matched = df_writeback_feedback_matched.append([{"id": entry.id, colname: category_from_feedback, "path": entry.to_dataframe_dictionary()["path"]}])
            catFromFeedbackCounter += 1

        if category_from_input or category_from_feedback:
            mapped_cat = category_from_input or category_from_feedback
            translated_mapped_cat = translate(translationfile, translations, language, mapped_cat)

            if not translated_mapped_cat:
                if not language == "en":
                    untranslatedCounter += 1
                translated_mapped_cat = mapped_cat

            setattr(entry, colname, translated_mapped_cat)
        else:
            df_writeback_feedback_missing = df_writeback_feedback_missing.append([{"id": entry.id, colname: blank_placeholder, "path": entry.to_dataframe_dictionary()["path"]}])
            has_unmatched_categories = True

    df_writeback_feedback = df_writeback_feedback.append(df_writeback_feedback_matched)
    df_writeback_feedback = df_writeback_feedback.append(df_writeback_feedback_missing)
    implicitly("prog.logger").info(f"{catFromInputFileCounter} of {len(dataset.rows)} entries have been assigned {colname}s based on their ids in {mapfile}")
    implicitly("prog.logger").info(f"{catFromFeedbackCounter} of {len(dataset.rows)} entries have been assigned {colname}s based on their ids in {feedbackfile}")
    implicitly("prog.logger").info(f"{(catFromFeedbackCounter+catFromInputFileCounter)-untranslatedCounter} of {catFromFeedbackCounter+catFromInputFileCounter} {colname}s have direct translations in {translationfile}, the rest inherits the english version")
    if catFromFeedbackCounter > 0:
        implicitly("prog.logger").info(f"[ NOTE ] when running the program with --initws, the file {feedbackfile} will be overwritten by the prototypical workspace and the manual entries may be lost. Consider merging them with the corresponding file of {input} in ./ws-static!")

    if has_unmatched_categories:
        api.implicitly("prog.logger").warning(f"[[ WARNING ]] : {len(df_writeback_feedback_missing)} entries in {input} could not be assigned {colname}s. To remedy this, edit the {colname}s manually in {feedbackfile}")


    # implicitly("prog.logger").info(f"writing feedbackfile with ids to {feedbackfile} with ids: {df_writeback_feedback['id'].tolist()}")
    df_writeback_feedback.to_csv(feedbackfile, quoting=csv.QUOTE_NONE, sep=flist.CSV_SEP, index=False, header=False)
    dataset.write_csv(output)
