#!/usr/bin/env python3

import os
import sys
import scriptlib; from scriptlib import Arg, Args, Scriptspec
# import plumbum; from plumbum import local

import flist
import flist_steps; from flist_steps import FListComponents

default_ws_location = flist.envdir("sandbox", "ws.local")


def FListProcess(workspace):
    _workspace = workspace[-1]
    components = FListComponents(_workspace)

    components.step_setup()

    source_step = "scsv_webdump"
    target_step = "merge_scsv"
    components.wscopy(f"--prefix=input/{target_step}/{source_step}/", f"data/{source_step}/*")

    source_step = "merge_scsv"
    target_step = "generate_html"
    components.step_merge_scsv(f"--output=output/{source_step}/{source_step}.csv", f"input/{source_step}/**/*")
    components.wscopy(f"--prefix=input/{target_step}/{source_step}/", f"output/{source_step}/*")

    # source_step = "scsv_CT2"
    # components.wscopy(f"--prefix=input/{target_step}/{current_step}/", "data/{current_step}/*")
    # components.step_scsv_ct2(f"--output=output/{current_step}")


# Scripting boilerplate {{{
script_handler = Scriptspec( __file__, Args([
        Arg.Keyval("workspace"), 
    ]), self_passed_args = [
        f"--workspace={default_ws_location}"
    ],
    kwargs_receiver = FListProcess
)

if __name__ == "__main__":
    script_handler.run(sys.argv[1:])

# }}}
