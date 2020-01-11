from pathlib import Path
import dataclasses; from dataclasses import dataclass, field
import typing; from typing import List, Dict, Any, Callable, Optional
import sys
import benedict; from benedict.dicts import benedict as bdict
import flist_api as api; from flist_api import implicitly

import plumbum; from plumbum.commands import BaseCommand
import flist_colmap
import flist_step_categories
import flist_step_CT2scsv
import flist_step_merge
import flist_step_tofinalform
import flist_step_tohtml
import flist_step_outputfilter

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
        processed = element
        if isinstance(processed, str):
            processed = processed.replace('${workspace}', str(implicitly("workspace").path))
        if isinstance(processed, str):
            processed = processed.replace('${workspace_template}', str(implicitly("workspace").template))
        if isinstance(processed, str):
            processed = processed.replace('${project}', str(Path(__file__).parent.parent))
        if isinstance(processed, str):
            try:
                topath = Path(processed)
                if topath.is_absolute():
                    processed = topath
            except:
                pass
        return processed

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

allsteps=[]
def registerStep(step: FlistStep):
    global allsteps
    allsteps.append(step)

def getStep(stepname: str):
    matched = [step for step in allsteps if step.name == stepname]
    if len(matched) == 0:
        raise Exception(f"could not find step with name {stepname}")
    return matched[0]

init_workspace = FlistStep(
            name = "init_workspace",
            callable = lambda : implicitly("workspace").recreated(),
            proto = {}
        )
registerStep(init_workspace);

ct2outputfilter_en = FlistStep(
    name="ct2outputfilter_en",
    callable = flist_step_outputfilter.PreprocessCT2,
    proto = bdict(input=None, output=None, language="en")
)
registerStep(ct2outputfilter_en)

ct2outputfilter_de = FlistStep(
    name="ct2outputfilter_de",
    callable = flist_step_outputfilter.PreprocessCT2,
    proto = bdict(input=None, output=None, language="de")
)
registerStep(ct2outputfilter_de)

CT2scsv_jct_en = FlistStep(
    name="CT2scsv_jct_en",
    callable = flist_step_CT2scsv.CreateCT2SCSV,
    proto = bdict(input=None, output=None, id_reference=None, toolname="JCT")
)
registerStep(CT2scsv_jct_en)

CT2scsv_jct_de = FlistStep(
    name="CT2scsv_jct_de",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="JCT")
)
registerStep(CT2scsv_jct_de)

CT2scsv_ct2_en = FlistStep(
    name="CT2scsv_ct2_en",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="CT2")
)
registerStep(CT2scsv_ct2_en)

CT2scsv_ct2_de = FlistStep(
    name="CT2scsv_ct2_de",
    callable = flist_step_CT2scsv.CreateCT2SCSV, 
    proto = bdict(input=None, output=None, id_reference=None, toolname="CT2")
)
registerStep(CT2scsv_ct2_de)

categories_ct2_en = FlistStep(
    name="categories_ct2_en", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="category", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="en")
)
registerStep(categories_ct2_en)

categories_ct2_de = FlistStep(
    name="categories_ct2_de", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="category", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="de")
)
registerStep(categories_ct2_de)

categories_jct_en = FlistStep(
    name="categories_jct_en", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="category", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="en")
)
registerStep(categories_jct_en)

categories_jct_de = FlistStep(
    name="categories_jct_de", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="category", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="de")
)
registerStep(categories_jct_de)

functionalities_jct_en = FlistStep(
    name="functionalities_jct_en", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="functionality", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="en")
)
registerStep(functionalities_jct_en)

functionalities_jct_de = FlistStep(
    name="functionalities_jct_de", 
    callable = flist_colmap.Map_Columns,
    proto = bdict(input=None, colname="functionality", translationfile=None, mapfile=None, output=None, feedbackfile=None, language="de")
)
registerStep(functionalities_jct_de)

merge_en = FlistStep(
    name="merge_en",
    callable = flist_step_merge.MergeImpl,
    proto = bdict(input=[], output=None)
)
registerStep(merge_en)

merge_de = FlistStep(
    name="merge_de",
    callable = flist_step_merge.MergeImpl,
    proto = bdict(input=[], output=None)
)
registerStep(merge_de)

tofinalform_en = FlistStep(
    name="tofinalform_en",
    callable = flist_step_tofinalform.CreateFinalForm,
    proto = bdict(input=None, output=None)
)
registerStep(tofinalform_en)

tofinalform_de = FlistStep(
    name="tofinalform_de",
    callable = flist_step_tofinalform.CreateFinalForm,
    proto = bdict(input=None, output=None)
)
registerStep(tofinalform_de)

tohtml_en = FlistStep(
    name="tohtml_en",
    callable = flist_step_tohtml.MakeHTML,
    proto = bdict(input=None, output=None, template_html=None)
)
registerStep(tohtml_en)

tohtml_de = FlistStep(
    name="tohtml_de",
    callable = flist_step_tohtml.MakeHTML,
    proto = bdict(input=None, output=None, template_html=None)
)
registerStep(tohtml_de)
