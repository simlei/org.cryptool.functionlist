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
import benedict; from benedict import benedict as bdict

class ArgToken(ABC):
    @abstractmethod
    def to_stringargs(self) -> str:
        pass

@dataclass 
class ArgTokenKeyval(ArgToken):
    key: str
    val: str
    op: str = "="

    def to_stringargs(self) -> [str]:
        return [ f"{self.key}{self.op}{self.val}" ]

@dataclass
class ArgTokenPositional(ArgToken):
    pos: int
    val: str
    
    def to_stringargs(self) -> List[str]:
        return [ self.val ]


def shift(restargs: List[str], shift_off: List[str], amount=1):
    if len(restargs) >= amount:
        shift_off.extend(restargs[0:amount])
    else:
        raise Exception("not enough args to shift so far!")
    return restargs[amount:]


@dataclass
class RawParse_Spec:
    
    kw_ids: List[str] = field(default_factory=list)
    sub_ids: List[str] = field(default_factory=list)
    aliases: Dict[str, str] = field(default_factory=dict)
    operators: List[str] = field(default_factory=lambda: ["=", "+=", "=[]"])
    any_keywords_allowed: bool = False

@dataclass
class RawParse_Result:
    initial: List[str]
    spec: RawParse_Spec
    localTokens: List[ArgToken]
    restargs: List[str]
    subCmd: str = None
    subCmdArgs: List[str] = field(default_factory=list)

def parse_raw_args(spec: RawParse_Spec, args: List[str]) -> RawParse_Result:
    i=0
    aliases = spec.aliases

    #result values
    tokens=[]
    subId=None
    subIdArgs=[]

    restargs=args.copy()
    parsed=[]
    pos=0

    kvmatch=re.compile(r"^--((\w|[._])+)("+"|".join([re.escape(lit) for lit in spec.operators])+")(.*)")              
    while len(restargs) > 0:
        arg=restargs[0] # type: str

        aliases = {k:v for k,v in spec.aliases.items() if arg.startswith(k)}
        if len(aliases) > 0:
            aliasing=list(aliases.items())[0]
            arg = arg.replace(aliasing[0], aliasing[1], count=1)

        if arg in spec.sub_ids:
            subId=arg
            restargs = shift(restargs, parsed, 1)
            break;

        match = kvmatch.match(arg)
        if match:
            k=match.group(1)
            op=match.group(3)
            v=match.group(4)
            if spec.any_keywords_allowed or k in spec.kw_ids:
                tokens.append(ArgTokenKeyval(key=k, val=v, op=op))
                parsed.append(arg)
                restargs = shift(restargs, parsed, 1)
                continue;

        pos = pos + 1
        tokens.append(ArgTokenPositional(pos=pos, val=arg))
        restargs = shift(restargs, parsed, 1)
    
    return RawParse_Result(
        initial=args,
        spec=spec, 
        localTokens=tokens, 
        subCmd=subId, 
        subCmdArgs=subIdArgs, 
        restargs=restargs
    )

def tokens_dictmerge(bd: bdict, tokens: List[ArgToken], positionalIds: List[str], varargsId="vargs"):
    result = {}
    posRemaining=positionalIds.copy()
    for token in tokens:
        print(f"{token=}")
        if isinstance(token, ArgTokenKeyval):

            if token.op == "=":
                print(f"dbg1: {bd}")
                bd.merge({token.key: token.val})
                print(f"dbg1: {bd}")

            elif token.op == "+=":
                if token.key in d:
                    if isinstance(bd[token.key], list):
                        bd[token.key].append(token.value)
                    else:
                        raise ArgparseException(f"parsing {token=} with not-applicable operator {token.op} into dict {bd}")
                else:
                    # TODO: uninitialized access, best guess
                    bd[token.key] = [token.value]
            else:
                raise ArgparseException(f"unknown operator: {op} in {token=}")

        elif isinstance(token, ArgTokenPositional):
            isVarargs = len(posRemaining) == 0
            if not isVarargs:
                id=posRemaining[0]
                posRemaining=posRemaining[1:]
                bd.merge({id: token.val})
            else:
                if not varargsId:
                    raise ArgparseException(f"cannot merge {token=} -- varargs id is not set (are varargs allowed?)")
                sub = bd.get(varargsId)
                if sub:
                    if not isinstance(sub, list):
                        raise ArgparseException(f"in merge-into vararg {token=}, {sub} is already of type {type(sub)}; for target {bd}")
                    else:
                        sub.append(token.val)
                else:
                    bd[varargsId] = [token.val]

def require_arg_key(d: dict, key: str, tpe=object):
    result = bdict(d).get(key, None)
    if result is None:
        raise ApiException(f"arg {key} is not present")
    if not isinstance(result, tpe):
        raise ApiException(f"arg {key} is not of required type {type}")
    return result


@dataclass
class ArgdictArgs:
    prog: str
    args: List[str]
    rawparse_result: RawParse_Result
    strdict: dict


class ArgdictSignature(ABC):

    def parse(self, args: List[str]) -> ArgdictArgs:
        parseresult = argdict_parse(self, args)
        conversion = self.convert_strdict(parseresult.strdict)
        if conversion is None:
            return parseresult
        return conversion


    def get_positional_ids(self) -> List[str]:
        return []

    def get_varargs_id(self) -> Optional[str]:
        return None

    def is_positional_id(self, id:str):
        return ( id in self.get_positional_ids() ) or ( id == self.get_varargs_id() )

    def is_keyval_id(self, id:str):
        return not self.is_positional_id(id)

    def make_rawparse_spec(self) -> RawParse_Spec:
        return RawParse_Spec()

    def make_default_argdict(self) -> dict:
        return {}

    def convert_strdict(self, d: dict):
        return None

def argdict_parse(sig: ArgdictSignature, args: List[str]) -> ArgdictArgs:
    prog = args[0]
    restargs = args[1:]
    rawresult = parse_raw_args(sig.make_rawparse_spec(), restargs)
    dictresult = bdict(sig.make_default_argdict())
    tokens_dictmerge(dictresult, rawresult.localTokens, sig.get_positional_ids(), sig.get_varargs_id())
    return ArgdictArgs(
        prog=prog, 
        args=restargs,
        rawparse_result=rawresult,
        strdict=dictresult
    )

class ApiException(Exception):
    pass

class ArgparseException(ApiException):
    pass




# @dataclass
# class ArgumentsBuilder(Arguments):
#     pos : List[Any]      = field(default_factory=list)
#     kw  : Dict[str, any] = field(default_factory=dict)
#     cont: ArgumentContrib

#     def get_positional(self):
#         return self.args

#     def get_keyword(self):
#         return self.kw

#     def add(contrib: ArgumentContrib):
#         self.contribs

# @dataclass
# class ArgumentContribKeyword:
#     id: str
#     value: str = None

#     # possible: =: keyval/
#     valQualifier: str = '='

#     @staticmethod
#     def Single(*thing: Any):
#         return ArgumentContribPos(list(thing))

#     @staticmethod
#     def Multi(ls: List[Any]):
#         return ArgumentContribPos(ls)

#     def contribute(builder: ArgumentsBuilder):
#         if self.value is not None:
#             existingVal = builder.kw[self.id]

#             if isinstance(builder.kw[self.id], dict):
#                 builder.kw[self.id]
#         builder.kw[self.id]


# @dataclass
# class ArgumentContribPos:
#     positionals: List[Any]

#     @staticmethod
#     def Single(*thing: Any):
#         return ArgumentContribPos(list(thing))

#     @staticmethod
#     def Multi(ls: List[Any]):
#         return ArgumentContribPos(ls)

#     def contribute(builder: ArgumentsBuilder):
#         builder.pos.append(self.positionals)



# class CommandStrlist(ABC):
    
#     @abstractmethod
#     def (args: List[str]):
#         pass


# class CmdlineCmd(ABC):

#     @abstractmethod
#     def execute_strings(self, args: List[str]):
#         pass

# class Workspace(ABC):
    
#     # implementors must take care to ensure, that get_base() exists and is a directory

#     @abstractmethod
#     def get_base() -> Path:
#         pass

#     def get_logs() -> Path:
#         return get_base() / "log"



