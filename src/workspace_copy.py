#!/usr/bin/env python3

import os
import sys
import flist
import shutil
import glob
import scriptlib; from scriptlib import Arg, Args, Scriptspec, expand_workspace_filelist

default_ws_location = flist.envdir("sandbox", "ws")


def Copy(files, prefix):
    dest_dir = os.path.dirname(prefix)
    os.makedirs(dest_dir, exist_ok=True)
    if(not os.path.isdir(dest_dir)):
        raise Exception(f"could not create Copy destination {dest_dir}")

    for file in files:
        shutil.copy(file, prefix + os.path.basename(file))


def Copy_Receiver(workspace, files, prefix):
    _workspace = workspace[-1]
    if not os.path.isdir(_workspace):
        raise Exception(f"{_workspace=} is not a directory")
    _prefix = prefix[-1]

    expanded = expand_workspace_filelist(_workspace, files)
    return Copy(
        expanded, 
        os.path.join(_workspace, _prefix)
    )

script_handler = Scriptspec( __file__, Args([
        Arg.Keyval("workspace"), 
        Arg.Positional("files"),
        Arg.Keyval("prefix")
    ]), self_passed_args = [
        f"--workspace={default_ws_location}", 
        f"--prefix=./"
    ],
    kwargs_receiver = Copy_Receiver
)

if __name__ == "__main__":
    script_handler.run(sys.argv[1:])
