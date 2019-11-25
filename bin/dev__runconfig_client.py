#!/usr/bin/env python3
import scriptlib

loaded = scriptlib.load_script_from("/home/simon/sandbox/featurelist/sandbox/bin/dev__runconfig.py")
loaded.spec.run(["--kv1=howdy", "arg1", "arg2"])
