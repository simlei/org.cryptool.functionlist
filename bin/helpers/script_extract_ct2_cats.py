#!/usr/bin/env python3

import sys
import os

import pandas

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


scsv_frame_ct2 = flist.SCSV_Dataset.Dataframe_From_Files([Path(__file__).parent.parent.parent / "ws-static/data/en/scsv_webdump/ct2.csv"])

def scsv_dump_file(tool, language):
    return Path(__file__).parent.parent.parent / f"ws-static/data/{language}/scsv_webdump/{tool.lower()}.csv"

def scsv_reference_file(tool):
    return scsv_dump_file(tool, "en")

def category_table_output_ws_static(tool, language):
    return Path(__file__).parent.parent.parent / f"ws-static/data/categories_{tool.lower()}.csv"

def category_table_output(tool, language):
    return Path(__file__).parent.parent.parent / f"ws/data/categories_{tool.lower()}.csv"

def load_legacy_and_infer_ids(tool, language) -> flist.SCSV_Dataset:
    file = scsv_dump_file(tool, language)
    referenceFile = scsv_reference_file(tool)

    dataset = flist.SCSV_Dataset.From_Dataframe(flist.SCSV_Dataset.Dataframe_From_Files([file]))
    dataset_reference = flist.SCSV_Dataset.From_Dataframe(flist.SCSV_Dataset.Dataframe_From_Files([referenceFile]))
    if len(dataset_reference.rows) != len(dataset.rows):
        raise io.FlistException(f"could not extract legacy categories for {file} automatically: reference file {referenceFile} has a mismatching number of entries.")

    entryIdx = 0
    for referenceEntry in dataset_reference.rows:
        # print(f"dbg: inferring {referenceEntry}")
        referenceEntry.infer_id_from_fields(tool)
        dataset.rows[entryIdx].id = referenceEntry.id
        entryIdx += 1

    return dataset

def legacy_scsv_to_catref(scsv: flist.SCSV_Dataset) -> pandas.DataFrame:
    df = scsv.to_dataframe()
    # df = df.drop(columns="path")
    df = df.drop(columns="how_implemented")
    df = df.drop(columns="functionality")
    return df


def extract_catref_file_in_wsstatic(tool, language):
    legacy_with_ids = load_legacy_and_infer_ids(tool, language)
    catref_df = legacy_scsv_to_catref(legacy_with_ids)
    output_wsstatic = category_table_output_ws_static(tool, language)
    output = category_table_output(tool, language)
    catref_df.to_csv(output_wsstatic, sep=flist.CSV_SEP, index=False, header=False, columns = ["id", "category", "path"])
    print(f"written to {output_wsstatic}")
    catref_df.to_csv(output, sep=flist.CSV_SEP, index=False, header=False, columns = ["id", "category", "path"])
    print(f"written to {output}")

extract_catref_file_in_wsstatic(tool = "CT2", language = "en")
extract_catref_file_in_wsstatic(tool = "JCT", language = "en")

# with open("/home/simon/sandbox/featurelist/ct_functionlist/ws-static/categories_ct2_en.csv", "wb") as opened:
#     for entry in scsv_ct2.

