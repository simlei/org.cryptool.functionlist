import os
import sys
import flist
import shutil
import argparse; from argparse import FileType
import flist_argtype as argtype
import flist_config as config
import pathlib; from pathlib import Path
import flist_io as io

project_root = Path(__file__).parent.parent
project_cfg  = project_root / "config.yaml"
ws_static_content_dir = project_root / "ws-static"

workspace = project_root / "ws"

def refresh_workspace():

    if workspace.exists():
        shutil.rmtree(workspace)
    os.makedirs(workspace)

    io.msg(f"populating workspace: {workspace}")
    for subelement in ws_static_content_dir.glob("*"):
        shutil.copytree(subelement, workspace / subelement.relative_to(ws_static_content_dir))


