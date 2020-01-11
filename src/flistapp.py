#!/usr/bin/env python

import plumbum; from plumbum import local
import argparse
import sys
import subprocess
import flist_io as io
import typing; from typing import List, Dict, Any, Optional
import dataclasses; from dataclasses import dataclass, field
import pathlib; from pathlib import Path
import abc; from abc import ABC, abstractmethod

import flist_api as api
import flist_steps as steps
import flist_files
import workspace as ws
import logging
    
from plumbum.commands import BaseCommand

class FlistProg(ws.WSProg, api.Prog):

    def __init__(self, stepsToRun):
        super().__init__()
        
        self.stepsToRun = stepsToRun
        self.context.names["prog.logger"] = io.logger
        self.context.names["prog.args_pos"] = []
        self.context.names["params.workspace.template"] = Path(__file__).parent.parent / "ws-static"

        self.context_processors += [
            api.ContextProcessorYamlConfig(Path(__file__).parent.parent / "config.yaml")
        ]

        self.steps = []

        for step in steps.allsteps:
            self.addStep(step)

    def runStep(self, step):
        step = self.context.names[f"step.{step.name}"] # type: steps.FlistStep
        step.perform()

    def addStep(self, step: steps.FlistStep, runByDefault=False):
        """
        Add a step to the program.
        Effectively, this registers a number of ContextProcessor instances that were made
        for the step, which work with the context w.r.t. to this step.
        
        The context will be populated with a set of dictionaries:
         - step.<stepname> -> the step object
         - config.step.<stepname> -> the config dictionary (yaml-parsed content) (string leafs)
         - params.step.<stepname> -> the parameters for invoking the step that result from the config namespace
        """

        self.steps += [ step ]

        self.context.names[f"step.{step.name}"] = step
        self.context.names[f"config.step.{step.name}"] = step.proto.copy()
        self.context.names[f"params.step.{step.name}"] = step.proto.copy() # todo

        self.context_processors += step.get_config_proc();

    def Main(self):
        self.context.names["state.currentStep"] = "__main__"
        self.context.make_implicit("state.currentStep")

        try:
            if not self.ws.path.exists():
                self.ws.recreated();
        except BaseException as e:
            print(f"Workspace could not be created at {self.ws.path}: {e}")
            sys.exit(100)

        mainLogger = logging.getLogger("Flist:Main")   ; mainLogger.setLevel (logging.INFO)
        mainLogger.addHandler(logging.FileHandler(self.ws.path / "log.txt"))
        mainLogger.addHandler(logging.StreamHandler(sys.stderr))
        mainLogger.info(f"Logging also to {self.ws.path / 'log.txt'}")
        self.context.names["prog.logger"] = mainLogger

        if(len(self.stepsToRun) == 0):
            for step in [steps.getStep(name) for name in self.context.names["config.defaultsteps"]]:
                self.context.names["state.currentStep"] = step.name
                self.runStep(step)
        else:
            for step in self.stepsToRun:
                self.context.names["state.currentStep"] = step.name
                self.runStep(step)

    def run_from_cmdline_call(self, argv: List[str] = None):
        try:
            super().run_from_cmdline_call(argv)
        except (io.FlistException or api.ApiException) as e:
            io.logFlistException(self.logger, e)
            exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    stepchoices = [step.name for step in steps.allsteps]
    parser.add_argument("steps", nargs="+", choices=stepchoices, help=f"step name sequence (of: {stepchoices}). When omitted, the defaultSteps from the config.yaml file are run.", metavar="STEPS")
    parser.add_argument("--initws", action="store_const", const=True, default=False)
    
    parsed = parser.parse_args(sys.argv[1:])
    # exit(0)
    if parsed.initws:
        parsed.steps = ["init_workspace"]
    elif parsed.steps == [None]:
        parsed.steps = []
    parsed.steps = [steps.getStep(stepname) for stepname in parsed.steps]

    prog = FlistProg(parsed.steps)
    prog.run_from_cmdline_call([])

