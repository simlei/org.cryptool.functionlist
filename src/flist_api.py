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
import inspect
import platform
import yaml

import logging;
import flist_args; from flist_args import RawParse_Spec, RawParse_Result, parse_raw_args

@dataclass
class DictContrib:
    key: str
    val: Any
    how: str="append"

    def apply(self, d: bdict):
        if not self.key in d:
            raise UnexpectedKey(f"Dict contrib for {self.key} not in target {d}")
        if isinstance(d[self.key], list):
            d[self.key] = d[self.key] + [ self.val ]
        
        d[self.key] = self.val
        

class Implicits(ABC):

    @abstractmethod
    def get(self, key):
        pass
    
class ContextImplicits(Implicits):

    def __init__(self, context):
        self.binds = bdict()
        self.context = context

    def add(self, contextkey, implicitkey):
        self.binds[implicitkey] = contextkey

    def get(self, key):
        if key in self.binds:
            return self.context.names.get(self.binds[key])

@dataclass
class DictImplicits(Implicits):
    d: dict

    def get(self, key, *args):
        return self.d.get(key, *args)

@dataclass
class Context(ABC):
    names: bdict
    implicits: ContextImplicits = field(default=None)

    def __post_init__(self):
        self.implicits = ContextImplicits(self)

    def make_implicit(self, ckey, ikey=None):
        self.implicits.add(ckey, ikey or ckey)

    def as_dict(self) -> dict:
        return self.names.copy()

    def getval(self, name) -> Any:
        return self[name]


class ContextProcessor(ABC):

    @abstractmethod
    def initialize(self, ctx: Context):
        pass

    @abstractmethod
    def process(self, ctx: Context) -> List[DictContrib]:
        pass

    def initialize(self, ctx: Context):
        pass

@dataclass
class ContextProcessorCopy(ContextProcessor):

    id_from: str
    id_to: str

    def process(self, ctx: Context) -> List[DictContrib]:
        if self.id_from in ctx.names:
            if isinstance(ctx[ self.id_from ], list):
                return [DictContrib(self.id_to, valsub) for valsub in ctx[ self.id_from ]]
            else:
                val = ctx.names[self.id_from]
                if val is not None:
                    return [DictContrib(self.id_to, val)]
                else:
                    return []

@dataclass
class ContextProcessorLambda(ContextProcessor):

    ids_in: List[str]
    id_out: str
    fun: Callable

    def process(self, ctx: Context) -> List[DictContrib]:
        # TODO: verification: existence in context
        inputs = [ctx.names.get(id) for id in self.ids_in]
        for inp in inputs:
            if inp is None:
                return []
        return [ DictContrib(self.id_out, self.fun(*inputs)) ]

@dataclass
class ContextProcessorForeach(ContextProcessor):

    id_in: str
    id_out: str
    fun: Callable

    def process(self, ctx: Context) -> List[DictContrib]:
        #TODO: check that it's a list
        implicitly("prog.logger").debug(f"in Foreach: {self=}")
        implicitly("prog.logger").debug(f"in Foreach: {ctx.names['config.step.merge_en']=}")
        implicitly("prog.logger").debug(f"in Foreach: {ctx.names['config.step'].keys()=}")
        result = []
        for thing in ctx.names[self.id_in]:
            val = self.fun(thing)
            result.append(DictContrib(self.id_out, val))
        return result

@dataclass
class ContextProcessorYamlConfig:
    path: Path

    def load(self):
        with open(self.path, "r") as input:
            try:
                return yaml.load(input)
            except Exception as e:
                raise ApiException(f"YAML config {self.path} could not be loaded: {e}")

    def process(self, ctx: Context) -> List[DictContrib]:
        yamlDict = self.load()
        pathSeparatedDict = bdict()
        # TODO: this probably shoud generate "linear dict contributions" but it's considered a static config block that is just copied over

        for k,v in yamlDict.items():
            pathSeparatedDict[k] = v

        return [ DictContrib("config", pathSeparatedDict, how=DictContrib.how_set) ]

@dataclass
class RawArgContextProcessor(ContextProcessor):
    def process(self, ctx: Context) -> List[DictContrib]:
        posIds = ctx.names["prog.args_positional"]
        specs = ctx.names["prog.argparsers"]
        args = ctx.names["prog.args"]

        restargs = args.copy()

        result = []
        parsers = [RawArgParser(s) for s in specs]
        for parser in parsers:
            restargs, contribs = parser.parse(restargs)
            result.extend(contribs)
        posIdsUsed = 0
        for token in result:
            if isinstance(token, flist_args.ArgTokenPositional):
                if len(posIds) > posIdsUsed:
                    id = posIds[len(posIdsUsed)]
                    posIdsUsed.append(id)
                    result.append( DictContrib("argdict." + id, token.val) )
                else:
                    result.append( DictContrib("argdict." + "varargs") )
            elif isinstance(token, flist_args.ArgTokenKeyval):
                result.append(DictContrib(token.key, token.val))
            else:
                raise Exception("incomplete case match on ArgToken! (bug)")

        return result

@dataclass
class DictContrib:
    how_append = "append"
    how_set    = "set"

    key: str
    val: Any
    how: str = how_append


    def apply(self, d: bdict):
        if self.how == DictContrib.how_append:
            if not self.key in d:
                raise UnexpectedKey(f"Dict contrib for {self.key} not in target {d}")
            if isinstance(d[self.key], list):
                d[self.key] = d[self.key] + [ self.val ]
            elif isinstance(d[self.key], dict):
                if not isinstance(self.val, dict):
                    raise UnexpectedKey(f"Dict contrib for {self.key} is not of type dict, but would have to be merged into target dict")
                d.update(self.val)
            else:
                d[self.key] = self.val
        elif self.how == DictContrib.how_set:
            d[self.key] = self.val



class Prog(ABC):

    def __init__(self):
        super().__init__()
        self._context = Context(bdict())

        self.context_processors = [] # type List[ContextProcessor]
        self.context_processors += [ RawArgContextProcessor() ]

        self.context.names["prog.__instance__"] = self
        self.context.make_implicit( "prog.__instance__", "Prog" )

        self.context.names["prog.args_positional"] = []
        self.context.names["prog.argparsers"] = []

        self.context.names["argdict.varargs"] = []
        self.context.names["prog.logger"] = logging.getLogger("Prog::Default")

        self.context.make_implicit("prog.logger")

    @property
    def logger(self) -> logging.Logger:
        return self.context.names["prog.logger"]

    @property
    def context(self) -> Context:
        return self._context

    def __process__(self):
        for processor in self.context_processors: # type: ContextProcessor
            self.logger.debug(f"Context: processing context with {processor}")
            processedContribs = processor.process(self.context) # type: List[DictContrib]

            for c in processedContribs:
                self.logger.debug(f"Context: applying {c}")
                c.apply(self.context.names)



    def run_from_cmdline_call(self, argv: List[str] = None):
        if not isinstance(argv, list):
            raise TypeError(f"cmdline call arguments must be provided as a list of strings")
        args = argv or sys.argv
        self.context.names["prog.arg0"] = args[0]
        self.context.names["prog.args"] = args[1:]

        self.__process__()
        self.Main()

# source: https://github.com/JadenGeller/Implicits
def _default_args(func):
    if platform.python_version().startswith("2."):
        return inspect.getargspec(func).defaults
    else:
        return [
            name 
            for name, parameter in inspect.signature(func).parameters.items()
            if parameter.default is not inspect.Parameter.empty
        ]

# returns None, if the specified key "name" in dict "d" is no "Context" object.
# else, return true
def _get_context(d, name):
    item = d.get(name)
    if item is None: 
        return False
    if isinstance(item, Context):
        return item
    else:
        return None

# returns None, if the specified key "name" in dict "d" is no "Context" object.
# else, return true
def _get_context_from_obj(o, name):
    if not hasattr(o, "context"):
        return None
    item = getattr(o, "context")
    if isinstance(item, Context):
        return item
    else:
        return None


def implicitly_or(key, default=None):
    try:
        return implicitly(key)
    except:
        return default

def implicitly(key):
    current_frame = None
    current_frame = inspect.currentframe()
    current_frame = current_frame.f_back if current_frame else None
    implicits_found = []
    while (current_frame := current_frame.f_back if current_frame else None) is not None:
        caller_locals = current_frame.f_locals
        obj = caller_locals.get("self")
        objcontext = _get_context_from_obj(obj, "context") if obj else None
        objimplicits = objcontext.implicits if objcontext else None
        localimplicits = _get_context(caller_locals, "implicit")

        objimplicits and implicits_found.append(objimplicits)
        localimplicits and implicits_found.append(localimplicits)
    result = None
    for impl in implicits_found:
        if result:
            break
        result = impl.get(key)
    if not result:
        raise ApiException(f"implicitly required {key=} not accessible")
    return result

class ApiException(Exception):
    pass

class UnexpectedKey(ApiException):
    pass

class ArgparseException(ApiException):
    pass



# Graveyard of Code :(

# @dataclass
# class FlistPyEntrypoint:
#     module: Any
#     init_args: List[str] = field(default_factory=list)
#     sig: ArgdictSignature = field(default=None)

#     def __post_init__(self):
#         self.sig = self.module.signature

#     def makeprog(self, additionalArgs: List[str]):
#         args = self.init_args.copy()
#         args = args + additionalArgs
#         print(additionalArgs) # dbg
#         prog = self.sig.parse([str(self)] + additionalArgs)
#         return prog
    
#     def __post_init__(self):
#         super().__init__();

# class PythonCallable(ABC):
#     @abstractmethod
#     def receiver() -> Callable:
#         pass
#     @abstractmethod
#     def positionalIds() -> List[str]:
#         pass
#     @abstractmethod
#     def allIds() -> List[str]:
#         pass
    
#     def invoke(self, objdict: dict):
#         bd=bdict(objdict)
#         posargs = [bd.get(posId) for posId in positionalIds]
#         kwargs  = bd.filter(lambda k: k in allIds and not k in positionalIds)


# @dataclass
# class ModuleCallable(PythonCallable):
#     module: Any
#     methodname: str

    




# def require_arg_key(d: dict, key: str, tpe=object):
#     result = bdict(d).get(key, None)
#     if result is None:
#         raise ApiException(f"arg {key} is not present")
#     if not isinstance(result, tpe):
#         raise ApiException(f"arg {key} is not of required type {type}")
#     return result


# @dataclass
# class ArgdictArgs:
#     prog: str
#     args: List[str]
#     rawparse_result: RawParse_Result
#     strdict: dict


# class ArgdictSignature(ABC):

#     def parse(self, args: List[str]) -> ArgdictArgs:
#         parseresult = argdict_parse(self, args)
#         conversion = self.convert_strdict(parseresult.strdict)
#         if conversion is None:
#             return parseresult
#         return conversion


#     def get_positional_ids(self) -> List[str]:
#         return []

#     def get_varargs_id(self) -> Optional[str]:
#         return None

#     def is_positional_id(self, id:str):
#         return ( id in self.get_positional_ids() ) or ( id == self.get_varargs_id() )

#     def is_keyval_id(self, id:str):
#         return not self.is_positional_id(id)

#     def make_rawparse_spec(self) -> RawParse_Spec:
#         return RawParse_Spec()

#     def make_default_argdict(self) -> dict:
#         return {}

#     def convert_strdict(self, d: dict):
#         return None

# def argdict_parse(sig: ArgdictSignature, args: List[str]) -> ArgdictArgs:
#     prog = args[0]
#     restargs = args[1:]
#     rawresult = parse_raw_args(sig.make_rawparse_spec(), restargs)
#     dictresult = bdict(sig.make_default_argdict())
#     tokens_dictmerge(dictresult, rawresult.tokens, sig.get_positional_ids(), sig.get_varargs_id())
#     return ArgdictArgs(
#         prog=prog, 
#         args=restargs,
#         rawparse_result=rawresult,
#         strdict=dictresult
#     )



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



