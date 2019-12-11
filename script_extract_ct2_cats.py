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


scsv_frame_ct2 = flist.SCSV_Dataset.Dataframe_From_Files([Path("/home/simon/sandbox/featurelist/ct_functionlist/ws/data/en/scsv_webdump/ct2.csv")])
dataset = flist.SCSV_Dataset.From_Dataframe(scsv_frame_ct2)
for row in dataset.get_rows():
    funct = row["functionality"]
    howimpl_payload = row["how_implemented"]
    how_implemented = f"CT2:{howimpl_payload}"
    normalizedpath = " \\ ".join([how_implemented] + row["path"])
    hash = flist.makeId(funct, normalizedpath, howimpl_payload)

    print(f"hash:{hash}", row)

# with open("/home/simon/sandbox/featurelist/ct_functionlist/ws-static/categories_ct2_en.csv", "wb") as opened:
#     for entry in scsv_ct2.

# || hash:69fda4c8 {'id': 'CT2:static:1', 'functionality': '3DES', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Modern Ciphers', 'Symmetric', 'DES'], 'category': '2) Modern Ciphers'}
# || hash:d080b739 {'id': 'CT2:static:2', 'functionality': '3DES Brute-Force Attack', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Cryptanalysis', 'Specific', 'KeySearcher'], 'category': '7) Modern Cryptanalysis'}
# || hash:140dee79 {'id': 'CT2:static:3', 'functionality': '3DES Brute-Force Attack', 'how_implemented': 'CT2:T', 'path': ['CT2:T', 'Cryptanalysis', 'Modern', 'Triple DES Brute-force Analysis'], 'category': '7) Modern Cryptanalysis'}
# || hash:9f99a795 {'id': 'CT2:static:4', 'functionality': 'Achterbahn', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Modern Ciphers', 'Symmetric', 'Achterbahn'], 'category': '2) Modern Ciphers'}
# || hash:bc606c12 {'id': 'CT2:static:5', 'functionality': 'Achterbahn', 'how_implemented': 'CT2:T', 'path': ['CT2:T', 'Cryptography', 'Modern', 'Symmetric', 'Achterbahn Cipher'], 'category': '2) Modern Ciphers'}
# || hash:d043a16a {'id': 'CT2:static:6', 'functionality': 'ADFGVX', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Classic Ciphers', 'ADFGVX'], 'category': '1) Classic Ciphers'}
# || hash:7b453c59 {'id': 'CT2:static:7', 'functionality': 'ADFGVX', 'how_implemented': 'CT2:T', 'path': ['CT2:T', 'Cryptanalysis', 'Classical', 'ADFGVX Cipher dictionary attack'], 'category': '1) Classic Ciphers'}
# || hash:5ec789a9 {'id': 'CT2:static:8', 'functionality': 'ADFGVX', 'how_implemented': 'CT2:T', 'path': ['CT2:T', 'Cryptography', 'Classical', 'ADFGVX Cipher'], 'category': '1) Classic Ciphers'}
# || hash:f5ad740f {'id': 'CT2:static:9', 'functionality': 'ADFGVX', 'how_implemented': 'CT2:W', 'path': ['CT2:W', 'Encryption', 'Decryption', 'Classic Encryption', 'Decryption', 'ADFGVX'], 'category': '1) Classic Ciphers'}
# || hash:2e103daf {'id': 'CT2:static:657', 'functionality': 'Zero Knowledge Protocol', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Protocols', 'Zero Knowledge Prover'], 'category': '13) Protocols'}
# || hash:8f2154a8 {'id': 'CT2:static:658', 'functionality': 'Zero Knowledge Protocol', 'how_implemented': 'CT2:C', 'path': ['CT2:C', 'Protocols', 'Zero Knowledge Verifier'], 'category': '13) Protocols'}
# || hash:5fde8b3a {'id': 'CT2:static:659', 'functionality': 'Zero Knowledge Protocol', 'how_implemented': 'CT2:T', 'path': ['CT2:T', 'Protocols', 'Zero Knowledge Protocol'], 'category': '13) Protocols'}
