#!/usr/bin/env python3
import logging
import benedict; from benedict.dicts import benedict as bdict

a1=bdict(a1v="2")
a2=dict(a2v="3")
a2["x.y"] = {"hi": "ho"}
a1["x.y"] = {"ha": "hi"}
# def foo(d):
#     bd = bdict(d)
#     bd["foo"] = "bar"
#     return bd

# inp = a1
# inp = foo(inp)
# print(f"{inp=}")

# inp = a2
# inp = foo(inp)
# print(f"{inp=}")

# print("x.y" in a2)
# print("x" in a2)
# print("x.y" in a1)
# print("x" in a1)
# print(a1)
# print(a2)

import flist_io as io
logging.basicConfig(level=logging.INFO)
l1 = logging.getLogger("flist")
def bla(blub: logging.Logger = None):
    (blub or l1).info("hi")
bla()
io.logException(l1, Exception("sdfsdf"))
