from pathlib import Path
import dataclasses; from dataclasses import dataclass, field
import typing; from typing import List, Dict, Any, Callable, Optional
import sys
import benedict; from benedict.dicts import benedict as bdict
import flist_api as api; from flist_api import implicitly

import plumbum; from plumbum.commands import BaseCommand

def RunStep(step_prog) -> bool:
    currentStep = step_prog
    proc = step_prog.popen(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr); 
    currentProc = proc
    proc.communicate(); 
    if proc.returncode != 0: 
        return False
    else:
        return True

@dataclass
class FlistStep:
    name: str
    callable: Callable
    proto: dict

    # args_pos: List[Any] = field(default_factory = list)
    # args_kw : Dict[str, Any] = field(default_factory = dict)

    def get_config_proc(self):
        """
        returns the context processor contributions for the step.
        describes how a dictionary provided by e.g. YAML config (string based)
        is transferred to the "params" space for the step.

        For flist steps, this is implemented by looking at the step param
        prototype, and specifying for each subelement to be transformed 
        according to FlistStep.CfgTransfer, where first-level lists are recursed into.
        """
        result = []
        for key in self.proto:
            if isinstance(self.proto[key], list):
                sublistproc = api.ContextProcessorForeach(f"config.step.{self.name}.{key}", f"params.step.{self.name}.{key}", FlistStep.CfgTransfer)
                result.append(sublistproc)
            else:

                elementproc = api.ContextProcessorLambda([f"config.step.{self.name}.{key}"], f"params.step.{self.name}.{key}", FlistStep.CfgTransfer)
                implicitly("prog.logger").debug(f"{elementproc=}")
                result.append( elementproc )

        return result

    @staticmethod
    def CfgTransfer(element: Any) -> Any:
        """
        Transfer the configuration (config.step) of a step
        to the parameters for invoking the step (params.step)

        Naively identifies paths in the config to be augmented to the workspace
        by looking at whether a string starts with "./"
        """
        if isinstance(element, str):
            if element.startswith("./"):
                #TODO: many more cases possible...
                return Path(implicitly("workspace").path / element)
            else:
                return element
        else:
            return element


    def perform(self, *args, **kwargs):
        # implicitly("prog.logger").debug(f"performing on {context}")
        prog = implicitly("Prog") # type: api.Prog
        callableKwargs = prog.context.names[f"params.step.{self.name}"]
        callablePosargs = []
        callableKwargs.update(kwargs)
        callablePosargs += args

        # implicitly("prog.logger").debug(f"on step.{self.name} invocation, {prog.context.names['params.step.'+self.name]=}")
        # implicitly("prog.logger").info(f"running step.{self.name}({callablePosargs} {callableKwargs})")
        implicitly("prog.logger").info(f"Step {self.name} is being run with args ({callablePosargs} {callableKwargs})")
        self.callable(*callablePosargs, **callableKwargs)

def flist_augment_cfgpath(ws: Path, cfgpath: str):
    if cfgpath.startswith("."):
        return ws / cfgpath
    else:
        return Path(cfgpath)


import flist_step_categories
import flist_step_CT2scsv
import flist_step_merge
import flist_step_tofinalform
import flist_step_tohtml

CT2scsv_jct_en = FlistStep(
    name="CT2scsv_jct_en",
    callable = flist_step_CT2scsv.CreateCT2SCSV,
    proto = bdict(input=None, output=None, id_reference=None, toolname="JCT")
)
CT2scsv_jct_de = FlistStep(
    name="CT2scsv_jct_de",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="JCT")
)
CT2scsv_ct2_en = FlistStep(
    name="CT2scsv_ct2_en",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="CT2")
)
CT2scsv_ct2_de = FlistStep(
    name="CT2scsv_ct2_de",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="CT2")
)
categories_ct2_en = FlistStep(
    name="categories_ct2_en", 
    callable = flist_step_categories.Add_Categories,
    proto = bdict(input=None, catfile=None, output=None, feedbackfile=None, language="en")
)
categories_ct2_de = FlistStep(
    name="categories_ct2_de", 
    callable = flist_step_categories.Add_Categories,
    proto = bdict(input=None, catfile=None, output=None, feedbackfile=None, language="de")
)
categories_jct_en = FlistStep(
    name="categories_jct_en", 
    callable = flist_step_categories.Add_Categories,
    proto = bdict(input=None, catfile=None, output=None, feedbackfile=None, language="en")
)
categories_jct_de = FlistStep(
    name="categories_jct_de", 
    callable = flist_step_categories.Add_Categories,
    proto = bdict(input=None, catfile=None, output=None, feedbackfile=None, language="de")
)
merge_en = FlistStep(
    name="merge_en",
    callable = flist_step_merge.MergeImpl,
    proto = bdict(input=[], output=None)
)
merge_de= FlistStep(
    name="merge_de",
    callable = flist_step_merge.MergeImpl,
    proto = bdict(input=[], output=None)
)
tofinalform_en = FlistStep(
    name="tofinalform_en",
    callable = flist_step_tofinalform.CreateFinalForm,
    proto = bdict(input=None, output=None)
)
tofinalform_de= FlistStep(
    name="tofinalform_de",
    callable = flist_step_tofinalform.CreateFinalForm,
    proto = bdict(input=None, output=None)
)
tohtml_en = FlistStep(
    name="tohtml_en",
    callable = flist_step_tohtml.MakeHTML,
    proto = bdict(input=None, output=None, template_html=None)
)
tohtml_de= FlistStep(
    name="tohtml_de",
    callable = flist_step_tohtml.MakeHTML,
    proto = bdict(input=None, output=None, template_html=None)
)
