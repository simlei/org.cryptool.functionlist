import dataclasses; from dataclasses import dataclass, field
import abc; from abc import ABC, abstractmethod
import pathlib; from pathlib import Path
import plumbum; from plumbum import local
import typing; from typing import List, Dict, Any, Callable, Optional
import glob
import sys
import os
import inspect
import argparse
import re
import benedict; from benedict.dicts import benedict as bdict

def shift(restargs: List[str], shift_off: List[str], amount=1):
    if len(restargs) >= amount:
        shift_off.extend(restargs[0:amount])
    else:
        raise Exception("not enough args to shift so far!")
    return restargs[amount:]

@dataclass
class RawParse_Spec:
    kw_ids: List[str] = field(default_factory=list)
    aliases: Dict[str, str] = field(default_factory=dict)
    any_keywords_allowed: bool = True

class ArgToken:
    @abstractmethod
    def to_stringargs(self) -> str:
        pass

@dataclass 
class ArgTokenKeyval(ArgToken):
    key: str
    val: str
    op : str = "="

    def to_stringargs(self) -> [str]:
        return [ f"{self.key}{self.op}{self.val}" ]

@dataclass
class ArgTokenPositional(ArgToken):
    pos: int
    val: str
    
    def to_stringargs(self) -> List[str]:
        return [ self.val ]

@dataclass
class RawParse_Result:
    initial: List[str]
    spec: RawParse_Spec
    tokens: List[ArgToken]
    restargs: List[str]


@dataclass
class RawArgParser():
    spec: RawParse_Spec
    
    def parse(self, args: List[str]) -> (List[str], List[ArgToken]):
        result = parse_raw_args(self.spec, args)
        return result.restargs, result.tokens

def parse_raw_args(spec: RawParse_Spec, args: List[str]) -> RawParse_Result:
    aliases = spec.aliases
    #result values
    tokens=[]
    restargs=args.copy()
    parsed=[]
    pos=0

    kvmatch=re.compile(r"^--((\w|[._])+)(=)(.*)")
    while len(restargs) > 0:
        arg=restargs[0] # type: str

        aliases = {k:v for k,v in spec.aliases.items() if arg.startswith(k)}
        if len(aliases) > 0:
            aliasing=list(aliases.items())[0]
            arg = arg.replace(aliasing[0], aliasing[1], count=1)

        match = kvmatch.match(arg)
        if match:
            k=match.group(1)
            v=match.group(4)
            if spec.any_keywords_allowed or k in spec.kw_ids:
                tokens.append(ArgTokenKeyval(key=k, val=v))
                parsed.append(arg)
                restargs = shift(restargs, parsed, 1)
                continue;

        pos = pos + 1
        tokens.append(ArgTokenPositional(pos=pos, val=arg))
        restargs = shift(restargs, parsed, 1)
    
    return RawParse_Result(
        initial =args,
        spec    =spec, 
        tokens  =tokens, 
        restargs=restargs
    )

# def tokens_dictmerge(bd: bdict, tokens: List[ArgToken], positionalIds: List[str], varargsId="vargs"):
#     result = {}
#     posRemaining=positionalIds.copy()
#     for token in tokens:
#         print(f"{token=}")
#         if isinstance(token, ArgTokenKeyval):

#             if token.op == "=":
#                 bd.merge({token.key: token.val})

#             elif token.op == "+=":
#                 if token.key in d:
#                     if isinstance(bd[token.key], list):
#                         bd[token.key].append(token.value)
#                     else:
#                         raise ArgparseException(f"parsing {token=} with not-applicable operator {token.op} into dict {bd}")
#                 else:
#                     # TODO: uninitialized access, best guess
#                     bd[token.key] = [token.value]
#             else:
#                 raise ArgparseException(f"unknown operator: {op} in {token=}")

#         elif isinstance(token, ArgTokenPositional):
#             isVarargs = len(posRemaining) == 0
#             if not isVarargs:
#                 id=posRemaining[0]
#                 posRemaining=posRemaining[1:]
#                 bd.merge({id: token.val})
#             else:
#                 if not varargsId:
#                     raise ArgparseException(f"cannot merge {token=} -- varargs id is not set (are varargs allowed?)")
#                 sub = bd.get(varargsId)
#                 if sub:
#                     if not isinstance(sub, list):
#                         raise ArgparseException(f"in merge-into vararg {token=}, {sub} is already of type {type(sub)}; for target {bd}")
#                     else:
#                         sub.append(token.val)
#                 else:
#                     bd[varargsId] = [token.val]

