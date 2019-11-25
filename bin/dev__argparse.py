#!/usr/bin/env python3

import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--foo", "-z")
parser.add_argument("--flag", "-f", action="store_const", const=True)
parser.add_argument("--noflag", "-!f", action="store_const", const=True)

def str2bool(v):
    if isinstance(v, bool):
       raise argparse.ArgumentTypeError("string expected")
    if v.lower() in ('1'):
        return True
    elif v.lower() in ('0'):
        return False
    else:
        raise argparse.ArgumentTypeError('expected either 0 or 1')

def str2boolstr(v):
    if isinstance(v, bool):
       raise argparse.ArgumentTypeError("string expected")
    if v.lower() in ('1'):
        return "1"
    elif v.lower() in ('0'):
        return "0"
    else:
        raise argparse.ArgumentTypeError('expected either 0 or 1')


parser.add_argument("--nice", type=str2boolstr, nargs='?',
                        const="1", default="0",
                        help="test bool")


parser.add_argument("--flag2", "-F2", default=False, type=bool)
# print(parser.parse_args(["--foo=blub", "--nice"]))
# print(parser.parse_args(["--foo=blub"]))
# print(parser.parse_args(["--foo=blub", "--nice=1"]))

parser2 = argparse.ArgumentParser()
parser2.add_argument("bla")
# parser2.add_argument("--bla", dest="bla")
parser2.add_argument("blubb", nargs="*")
parser2.add_argument("blubb2", nargs="*")
# print(parser2.parse_args(["positional1"]))
# print(parser2.parse_args(["positional2", "--bla=positional, overridden"]))
# print(parser2.parse_intermixed_args(["bla: positional, overridden, 2", "positional1", "4"]))

parser3 = argparse.ArgumentParser()
parser3.add_argument("-D", action="append", dest="D")
parser3.add_argument("varargs", nargs="*")
# print(parser3.parse_intermixed_args(["-D=--flag1", "abc", "-D", "pos_for_D", "-Dpos2ForD"]))

parser4 = argparse.ArgumentParser()
parser4.add_argument("-D", action="append", dest="d")
parser4.add_argument("varargs", nargs="*")
print(parser4.parse_intermixed_args(["-D=--flag1", "abc", "-D--pos_for_d"]))


# print(sys.version_info)

# print(parser2.parse_args(["positional2", "--bla=ho"]))

