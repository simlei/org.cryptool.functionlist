#!/usr/bin/env python3

import os
import sys
import flist
import shutil
import scriptlib; from scriptlib import Arg, Args, Scriptspec

default_data_dir = flist.envdir_existing("sandbox", "data")
default_ws_location = flist.envdir("sandbox", "ws")

def CreateFreshWorkspace(workspace, data):
    _workspace = workspace[-1]
    _data = data[-1]
    print(f"FList: working with: {_workspace=}, {_data=}")
    if os.path.exists(_workspace):
        shutil.rmtree(_workspace)
    os.makedirs(_workspace)

    shutil.copytree(_data, os.path.join(_workspace, "data"))

script_handler = Scriptspec(
    __file__, 
    Args([
        Arg.Keyval    ("workspace"         ), 
        Arg.Keyval    ("data"         ), 
    ]),
    self_passed_args = [
        f"--workspace={default_ws_location}", 
        f"--data={default_data_dir}"
    ],
    kwargs_receiver = CreateFreshWorkspace,
)

if __name__ == "__main__":
    script_handler.run(sys.argv[1:])

