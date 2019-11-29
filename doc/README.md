# User documentation

Current capability:

- process files from [data/scsv_webdump/](data/scsv_webdump/)
- process files from [data/scsv_CT2](data/scsv_CT2/)
- merge them into `{workspace}/all_merged.csv`
- generate "final form" for export into phpMyAdmin `{workspace}/all_final.csv`

## Steps

This is done through the following "steps":

- workspace setup: --  `src/flist_step_setup.py`
- merging of "SCSV" files into a "MCSV" file -- `src/flist_step_merge.py`
- creation of a "final" csv file that matches the SQL database format: `src/flist_step_tofinalform`

These steps are python programs that can be executed on the command line. They take arguments (see below) but can be used without arguments too -- then, they follow "standard procedure" as dictated by `flist.config`. Especially, they work in the default "workspace".

These three steps are Python scripts that depend upon `src/flist.python` as the common library. They are usable completely independently and do not even depend on a workspace present -- by virtue of the common "workspace" base (see below), defaults are available for everything.

A full program run is executed with `bin/flist`, which does little more than run the default set of steps (configurable) in turn, delegating arguments given to the steps. For targeting a step with an argument, --{step}:{argument} can be used. The workspace argument is automatically delegated to all steps.

`{project-home}/bin/flist --workspace=ws2 --merge:data/scsv_webdump/CT1.csv` will run the whole thing, but ONLY with CT1.csv as SCSV data source.

Each step and `bin/flist` support the `--help` command line argument. This serves as documentation of what these arguments do.
A printout of these `--help` outputs and examples can be consulted in the [Command-line API](doc/command-line.md) reference.

## Config

The configuration of the default behavior of `bin/flist` and `src/step_*.py` is done through editing `config.yaml` in the root of this repository. Command line arguments override defaults. The format is YAML.

<!-- TODO: expand, explain correspondence to command-line parameters -->

## Data

<!-- TODO: to be expanded upon. Data format etc. -->
<!-- TODO: explain "SCSV", "MCSV" -->
