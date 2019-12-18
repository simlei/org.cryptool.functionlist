#!/usr/bin/env python3

import pandas
import pathlib; from pathlib import Path
import re
import flist

df_de = pandas.read_csv(Path(__file__).parent / "webdump_german_table.csv", sep=";")
df_de.fillna("", inplace=True)


df_de_jct = df_de[~ df_de["path_jct"].eq("")]
df_de_ct1 = df_de[~ df_de["path_ct1"].eq("")]
df_de_ct2 = df_de[~ df_de["path_ct2"].eq("")]
df_de_cto = df_de[~ df_de["path_cto"].eq("")]


lang = "de"

def split_it(ct, df):
    running = 0
    result = flist.SCSV_Dataset()

    for i,row in df.iterrows():
        pathstr = row[f"path_{ct}"]
        paths = pathstr.split('<br/>')
        for pathsplit in paths:
            running = running+1

            pathmatch = re.match
            if ct == "ct2" or ct == "jct":
                if m := re.match(r"^\s*\[(\w)\]\s*(.*)", pathsplit):
                    how_implemented = m.group(1)
                    restpath = m.group(2).strip()
                else:
                    raise Exception(f"{ct} path {pathsplit} in {row=} has no leading how_implemented indicator")
            else:
                how_implemented = "X"
                restpath = pathsplit.strip()

            path = f"{ct.upper()}:{how_implemented} \\ {restpath}"
            id = f"{ct.upper()}:{lang}:static:{running}"
            functionality = row["function"]
            category = row["category"]

            result.rows.append(flist.SCSV_Entry.From_Dataframe_Row(
                {
                 "id":id,
                 "category":category,
                 "how_implemented" : how_implemented,
                 "functionality" : functionality,
                 "path" : path 
                }
            ))
    # print(result.to_dataframe().to_string())
    result.write_csv(Path(__file__).parent / f"ws-static/data/de/scsv_webdump/{ct}.csv")

# print(df_de_ct2)
# split_it("ct1", df_de_ct1)
split_it("ct2", df_de_ct2)
# split_it("cto", df_de_cto)
# split_it("jct", df_de_jct)
