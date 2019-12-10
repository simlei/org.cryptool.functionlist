#!/usr/bin/env python3
# vim: ft=python

import sys
import os
import re

from typing import List
import dataclasses
from dataclasses import dataclass, field
import pandas
from plumbum import local
import flist

# import flist

# print(scsv_cto_frame)
# print(scsv_cto_frame[["functionality", "path"]])
# for entry in scsv_cto_frame[:]:
#     print("entry: " + str(entry))

# runspace_refresh = local["make_exec_space"]
# print(refresh_exec_space())

pandas.set_option('display.max_rows', 999)

testDataframe=flist.SCSV_Dataset.Dataframe_From_File(flist.envdir("scsv", "CTO.csv")) # type: pandas.DataFrame

testEntry = flist.SCSV_Entry(id="id", functionality="f", path=["p1"], category="cat", how_implemented="how")
testDataframe=testDataframe.append([dataclasses.asdict(testEntry)])

# print(testDataframe.to_string())

# for item in flist.SCSV_Dataset.From_Dataframe(testDataframe).get_entries():
#     print(item)
