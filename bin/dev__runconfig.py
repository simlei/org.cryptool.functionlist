#!/usr/bin/env python

import sys
import scriptlib
from scriptlib import Arg, Args, Scriptspec
import plumbum

def InterfaceMainMethod(parsedCfg, outfile):
    """
    only exemplary
    This is the method which is most likely be used by other python scripts -- no need to detour into string arguments
    However, the conversion from string arguments to objects is clear this way and this is a true hybrid between bash-style scripts and a reusable lib

    """
    pass

def MainArgsReceiver(kv1, flag1, pos, posN, D):
    """
    a receiver like this parses the strings that were split up into different variables by argparse
    and may pass it to a "true" interface / library method like InterfaceMainMethod
    """
    print(f"MainArgsReceiver({kv1=}, {flag1=}, {pos=}, {posN=}, {D=})")

def MainArgsReceiver2(**parsedKWArgs):
    """
    a receiver like this parses the strings that were split up into different variables by argparse
    and may pass it to a "true" interface / library method like InterfaceMainMethod

    This is the **kwargs variant, useful for fast prototyping; clients can call it with script-argument semantics via keywordargs
    """
    print(f"MainArgsReceiver2({parsedKWArgs=})")

script_handler = Scriptspec(
    __file__, 
    Args([
        Arg.Keyval    ("kv1"         ), 
        Arg.Flag      ("flag1"       ), 
        Arg.Delegate  ("D"           ), 
        Arg.Positional("pos", nargs=1), 
        Arg.Positional("posN"        )
    ]),
    self_passed_args = [
        "--kv1=Default",
        "--flag1=0", 
        "-D--blub"
    ],
    kwargs_receiver = MainArgsReceiver2,
)

if __name__ == "__main__":
    script_handler.run(sys.argv[1:])

