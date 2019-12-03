#!/usr/bin/env python3

import yaml
import dataclasses; from dataclasses import dataclass
import abc; from abc import ABC, abstractmethod
import pathlib; from pathlib import Path
import plumbum; from plumbum import local
import typing; from typing import List, Dict, Any, Callable
import argparse
import flist_argtype as argtype

import flist_io as io

project_root = Path(__file__).parent.parent
project_cfg  = project_root / "config.yaml"
project_ws_static_content_dir = project_root / "ws-static"

@dataclass
class FlistConfig:
    workspace: Path

def make_state(configobj, ws=None):
    current_ws = ws or project_root / "ws"
    fsobj = FlistFilesystem(current_ws, project_ws_static_content_dir)

    default_merge = MergeConfig(
        inputs = [current_ws / relpath for relpath in configobj["merge"]["input"]],
        output = current_ws / configobj["merge"]["output"]
    )
    default_ct2scsv = CT2SCSVConfig(
        input = current_ws / configobj["CT2scsv"]["input"],
        output = current_ws / configobj["CT2scsv"]["output"]
    )
    default_jct2scsv = JCT2CSVConfig(
        input = current_ws / configobj["JCTscsv"]["input"],
        output = current_ws / configobj["JCTscsv"]["output"]
    )
    default_tofinalform = MergeConfig(
        inputs = [current_ws / relpath for relpath in configobj["tofinalform"]["input"]],
        output = current_ws / configobj["tofinalform"]["output"]
    )
    default_tohtml = MergeConfig(
        inputs = [current_ws / relpath for relpath in configobj["tohtml"]["input"]],
        output = current_ws / configobj["tohtml"]["output"]
    )
    state = FlistProgramState(
        fs = fsobj, 
        defaults = FlistDefaults(
            merge = default_merge,
            ct2scsv = default_ct2scsv,
            jctscsv = default_jctscsv,
            tofinalform = default_tofinalform,
            tohtml = default_tohtml
        )
    )
    return state


# parses args of a step, by taking its parser and wrapping it.
# returns a tuple: (parsed, flistProgramState)
def parse_args(args, subparse_contrib):
    # one parser run just for getting the --workspace AND the --help right. 
    # client method gets called 2 times, but no way around it
    cfg = parse_cfg()

    state = make_state(cfg)
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=argtype.DirPath, default=(project_root / "ws"))
    subparse_contrib(parser, state)
    parsed = parser.parse_args(args)
    state = make_state(cfg, parsed.workspace)
    
    # re-parse, with workspace (and thus, global cfg) resolved and suppliable to the subparser
    # parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=argtype.DirPath, default=(project_root / "ws"))
    subparse_contrib(parser, state)
    parsed = parser.parse_args(args)
    return parsed, state

def parse_cfg():
    with open(project_cfg, "r") as input:
        try:
            return yaml.load(input)
        except Exception as e:
            io.err("The config file (config.yaml) could not be read correctly and is probably malformed. Please refer to https://en.wikpedia.org/YAML for the file format and git checkout config.yaml for a sane state of the file.")
            exit(3)

@dataclass
class FlistFilesystem:
    workspace: Path
    ws_static_content_dir: Path

@dataclass
class JCTSCSVConfig:
    input: Path
    output: Path

@dataclass
class CT2SCSVConfig:
    input: Path
    output: Path

@dataclass
class MergeConfig:
    inputs: List[Path]
    output: Path

@dataclass
class TofinalformConfig:
    inputs: List[Path]
    output: Path

@dataclass
class TohtmlConfig:
    inputs: List[Path]
    output: Path

@dataclass
class FlistDefaults:
    merge: MergeConfig
    ct2scsv: CT2SCSVConfig
    jctscsv: JCTSCSVConfig
    tofinalform: TofinalformConfig
    tohtml: TohtmlConfig

@dataclass
class FlistProgramState:
    fs: FlistFilesystem
    defaults: FlistDefaults
