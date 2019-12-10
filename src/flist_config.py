#!/usr/bin/env python3

import yaml
import dataclasses; from dataclasses import dataclass
import abc; from abc import ABC, abstractmethod
import pathlib; from pathlib import Path
import plumbum; from plumbum import local
import typing; from typing import List, Dict, Any, Callable
import argparse
import flist_argtype as argtype
import flist_files

import flist_io as io


# def parse_cfg():
#     with open(project_cfg, "r") as input:
#         try:
#             return yaml.load(input)
#         except Exception as e:
#             io.err("The config file (config.yaml) could not be read correctly and is probably malformed. Please refer to https://en.wikpedia.org/YAML for the file format and git checkout config.yaml for a sane state of the file.")
#             exit(3)

# globalcfg = parse_cfg()

# def require_cfg(subkey):
#     if not subkey in globalcfg:
#         raise io.FlistException(f"no config.yaml key present for step {subkey}!")
#     return globalcfg[subkey]


# print(parse_cfg())
# print(type(parse_cfg()["merge_en"]))
# print(parse_cfg()["msdf"])
