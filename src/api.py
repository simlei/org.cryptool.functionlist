import dataclasses; from dataclasses import dataclass
import abc; from abc import ABC, abstractmethod
import pathlib; from pathlib import Path
import plumbum; from plumbum import local
import typing; from typing import List, Dict, Any, Callable

"""
An API for a utility consists of
 - a number of entry points (Prog)
 - a designated main entry point (api.progMain)
 - a common configuration object which connects the entry points.

Each entry point can be called independently as a standalone program. Each API has however
a "Defaults" configuration class that is common to all entry points w.r.t. to their argument parsing.
This is designed to allow proper concertation of the entry points while requiring an overall lower
amount of configuration parameters per single call.

A program with multiple entry points has to maintain state in many cases.
The method of choice to communicate state while keeping a low configuration profile
is a directory in the file system, commonly called "workspace". It serves two purposes:

- Make path configuration (e.g. for defaults, on the command line) relative and therefore, transferable 
  between different machines and setups.
- Make the state shareable with a single, all-encompassing method: the passing of a "workspace" path.
  The file system is arguably the lowest common denominator between tools of all varieties, which makes
  it a good general-purpose choice. It is also a tree structure, therefore able to accomodate both simple and very complex use cases.
"""



class Entrypoint(ABC)
"""
The executable is specified as file system path relative to the repository 
or as the name of an executable that gets resolved through the system PATH. 
Absolute paths do not work well between different machines
and are therefore not explicitely supported. 

Traditionally, entry points are single python files, and their command line execution
is `python <file> <args>`. 
More generally, this can be expressed as `<executable> <stub> <args>` This semantic is represented by the `ScriptEntrypoint` class.
Multiple entry points are possible per script; they are pre-configured with arguments (the argument "stub").
The executable for a python script is, lacking `#!` (shebang) semantics on non-unix systems, the "python" executable. The python file is already a "stub" argument; it is however directly accessible by representation 
though `PythonEntryPoint`
"""

    @abstractmethod
    def get_localcmd(self) -> plumbum.local.LocalCommand:
        pass

    @abstractmethod
    def get_executable_coord(self) -> str:
        pass

    def is_coord_a_path(self) -> bool:
        cmd=local["ls"]
        cmd.executable
        return self.get_localcmd()
        # return '/' in self.get_executable_coord() or "\\" in self.get_executable_coord()

    def is_coord_for_syspath_resolution(self) -> bool:
        return not self.is_coord_a_path()

    def get_localcmd() -> plumbum.local.LocalCommand:
        return plumbum.local

@dataclass
class Prog(ABC):

    id: str
    cmd: local.LocalCommand
    main: Callable


    def __post_init__(self):
        self.cmd = local.LocalCommand

    def commandline(self, *pargs):
        return self.cmd(*pargs)


