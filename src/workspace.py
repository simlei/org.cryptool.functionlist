import dataclasses; from dataclasses import dataclass, field
import abc; from abc import ABC, abstractmethod
import pathlib; from pathlib import Path
import shutil
import plumbum; from plumbum import local
import typing; from typing import List, Dict, Any, Callable, Optional
import glob
import sys
import os
import inspect
import argparse
import re
import benedict; from benedict.dicts import benedict as bdict
import flist_argtype

import flist_api as api; from flist_api import implicitly

import flist_args
import flist_argtype as argtype

@dataclass
class Workspace:
    path: Path
    template: Optional[Path] = None
    
    @property
    def ensured(self):
        return ensure_workspace(self.path, self.template)

    def recreated(self):
        return recreate_workspace(self.path, self.template)

class WSProg(api.Prog):
    
    def __init__(self):
        super().__init__()

        self.context.make_implicit("workspace")

        self.context.names["argdict.workspace.path"] = None
        self.context.names["argdict.workspace.template"] = None


        # todo: these should not be the default parameters, do not make sense for a library.
        self.context.names["params.workspace.path"] = Path(__file__).parent.parent / "ws"
        self.context.names["params.workspace.template"] = Path(__file__).parent.parent / "ws_static"

        self.context.names["workspace"] = Workspace(self.context.names["params.workspace.path"], self.context.names["params.workspace.template"])

        self.context.names["prog.args_positional"]
        self.context_processors += [ 
            api.ContextProcessorLambda(["argdict.workspace.path"], "params.workspace.path", Path),
            api.ContextProcessorLambda(["argdict.workspace.template"], "params.workspace.template", argtype.DirPathExisting), 
            api.ContextProcessorLambda(["params.workspace.path", "params.workspace.template"], 
                                       "workspace",
                                       Workspace)
        ]



    @property
    def ws(self) -> Workspace:
        # TODO: validate that workspace is set
        return self.context.names["workspace"]



def ensure_workspace(path: Path, template: Optional[Path] = None):
    if path.exists():
        if path.is_file():
            raise Exception(f"Workspace is present but is pointing to a file {path}")
        return Workspace(path, template)
    else:
        return recreate_workspace(path, template)

def recreate_workspace(path: Path, template: Optional[Path] = None):

    if template:
        if not template.exists():
            raise api.ArgparseException(f"workspace: template dir {template} does not exist")
    if path.exists():
        shutil.rmtree(path)
    os.makedirs(path)

    if template is not None:
        for subelement in template.glob("*"):
            # implicitly("prog.logger").debug(f"shutil.copytree({subelement}, {path / subelement.relative_to(template)})")
            if subelement.is_dir():
                shutil.copytree(subelement, path / subelement.relative_to(template))
            else:
                shutil.copy(subelement, path / subelement.relative_to(template))

    return Workspace(path, template)


