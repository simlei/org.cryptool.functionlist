import glob
import sys
import os
import inspect
import argparse
import dataclasses; from dataclasses import dataclass, field
import abc; from abc import ABC, abstractmethod
import typing; from typing import List, Any, Dict

def str2boolstr(v):
    if isinstance(v, bool):
       raise argparse.ArgumentTypeError("string expected")
    if v.lower() in ('1'):
        return "1"
    elif v.lower() in ('0'):
        return "0"
    else:
        raise argparse.ArgumentTypeError('expected either 0 or 1')

def str2bool(v):
    if isinstance(v, bool):
       raise argparse.ArgumentTypeError("string expected")
    if v.lower() in ('1'):
        return True
    elif v.lower() in ('0'):
        return False
    else:
        raise argparse.ArgumentTypeError('expected either 0 or 1')

@dataclass
class ArgparseAddition:
    # nargs: str = None
    # const: Any = None
    # default: Any = None
    # help: str = None
    # type: Any = None
    # action: Any = None
    varargs: List[Any] = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)

    def __post_init__(self):
        if len(self.varargs) == 0: raise "not enough arguments for ArgparseAddition: must have --<id>"

    def applyToParser(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        # print(f"add_argument {self.varargs}, {self.kwargs}")
        parser.add_argument(*self.varargs, **self.kwargs)

# signature elements:
# positional single (regular), varargs ()
# keyword
# flags translate to keyword with implied --flag=true
class ArgSpec(ABC):
    @abstractmethod
    def get_id() -> str:
        pass

    @abstractmethod
    def get_parser_additions(self) -> List[ArgparseAddition]:
        pass

# issued by a program
class Signature(ABC):
    @abstractmethod
    def get_argspecs(self) -> List[ArgSpec]:
        pass

    @abstractmethod
    def make_argparser(self) -> argparse.ArgumentParser:
        pass

@dataclass
class Args(Signature):
    argspecs: List[ArgSpec]
    def get_argspecs(self): return self.argspecs

    def make_argparser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        for additions in self.get_argspecs():
            for addarg in additions.get_parser_additions():
                addarg.applyToParser(parser)
        return parser


def is_receiver_kwargs(receiver):
    has_kwargs = any(param for param in inspect.signature(receiver).parameters.values() if param.kind == param.VAR_KEYWORD)
    is_only_arg = len(inspect.getargspec(receiver).args) == 0

@dataclass
class Scriptspec:
    executable: str
    signature: Signature
    kwargs_receiver: Any
    parser: argparse.ArgumentParser = field(init=False, repr=False)
    self_passed_args: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.parser = self.signature.make_argparser()

    def run(self, args=None):
        _args = self.self_passed_args + (args or [])
        parsed = self.parser.parse_intermixed_args(_args)
        # print(f"calling {self.kwargs_receiver}({vars(parsed)})")
        return self.kwargs_receiver(**vars(parsed))

def load_script_from(path):
    import importlib
    import importlib.util
    import random

    module_name = "script_" + str(random.randint(1,99999))
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return ScriptModule(module, module.script_handler)

@dataclass 
class ScriptModule:
    module: Any
    spec: Scriptspec

class Arg:

    @dataclass
    class Keyval():
        id: str
        parserAdditions: List[ArgparseAddition] = field(default_factory=list, repr=False, init=False)

        def get_id() -> str:
            return self.id;

        def __post_init__():
            pass

        def __post_init__(self):
            self.parserAdditions.append(ArgparseAddition(
                    [f"--{self.id}"], 
                    {"action":"append", "dest":f"{self.id}"}
                ))
        
        def get_parser_additions(self) -> List[ArgparseAddition]: return self.parserAdditions

    # TODO: works only for single-char ids
    @dataclass
    class Delegate():
        id: str
        parserAdditions: List[ArgparseAddition] = field(default_factory=list, repr=False, init=False)

        def get_id() -> str:
            return self.id;

        def __post_init__():
            pass

        def __post_init__(self):
            self.parserAdditions.append(ArgparseAddition(
                    [f"-{self.id}"], 
                    {"action":"append", "dest":f"{self.id}"}
                ))

        def get_parser_additions(self) -> List[ArgparseAddition]: return self.parserAdditions

    @dataclass
    class Flag():
        id: str
        parserAdditions: List[ArgparseAddition] = field(default_factory=list, repr=False, init=False)

        def get_id() -> str:
            return self.id;
        
        def __post_init__(self):
            self.parserAdditions.append(ArgparseAddition(
                    [ f"--{self.id}" ], 
                    { "type": str2bool, "nargs": "?", "const": "1", "default": "0"}
                ))
        def get_parser_additions(self) -> List[ArgparseAddition]: return self.parserAdditions

    @dataclass
    class Positional:
        id: str
        nargs: int = -1
        parserAdditions: List[ArgparseAddition] = field(default_factory=list, repr=False, init=False)

        def get_id() -> str:
            return self.id
        
        def __post_init__(self):
            self.parserAdditions.append(ArgparseAddition(
                    [ f"{self.id}" ], 
                    {} if self.nargs == 1 else { "nargs": self.nargs if self.nargs > 0 else '*'}
                ))

        def get_parser_additions(self) -> List[ArgparseAddition]: return self.parserAdditions

def expand_workspace_filelist(workspace, files):
    expanded = [glob.glob(os.path.join(workspace,f), recursive=True) for f in files]
    flattened = [file for sublist in expanded for file in sublist]
    return flattened

