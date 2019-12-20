# Developer documentation

## Workspace directory

TODO: bring up-to-date, doc_misc into doc/misc, refer to workspace sample

The so-called "Workspace" connects all the single steps. It can be specified for each step separately via `--workspace <WS-dir>` argument, or be completely left out. In the latter case, the workspace defaults to the "ws" directory next to the "src" directory in the project home folder.

It looks like this, after all steps have been run (19/11/28):

```
ws/
├── all_final.csv    : the file that corresponds to the website input
├── all_merged.csv   : the file that contains the "raw", but merged content from different CT projects
└── data             : by default, a clone of /data in this repository
    ├── scsv_CT2     : contains the dynamically generated csv files of CT2
    │   └── FunctionList-en.csv
    └── scsv_webdump : contains the data that was copied from the website; the most up to date legacy dataset
        ├── CT1.csv
        ├── CT2.csv
        ├── CTO.csv
        └── JCT.csv
```

The data folder is by default a copy of the "data" dir next to the "src" dir of this repository. It may also be linked, or the files in it be specified to be loaded from any location. In most cases though, it is most convenient to run `src/flist_step_setup.py --workspace <if-left-out-defaults-to-ws-dir>` which sets up a workspace completely from scratch.
# TODO next

- CT2 paths in the final csv do not have a `[C]`-like path prefix
- convert `data/scsv_CT2/*` into properly formatted csv and push it into `flist_step_merge`, too. This is the prototype for processing dynamic output of the CrypTools (JCT to follow)
- generate a local version of the webpage for simulating the eventual behavior

## More TODO after these steps check out

- let JCT generate output that augments the legacy data in [data/scsv_webdump/JCT.csv](data/scsv_webdump/JCT.csv), with the goal to improve that functionality to the point of replacing that file entirely (as will have happened already with CT2)
- have CT2 and JCT generate translation files
    - incorporate these into the pipeline, so that a german translation of the "final" `ws/all_final.csv` file is generated

See also the [comprehensive overview over findings](todo.md). in the (formerly manually maintained) web-dump database
