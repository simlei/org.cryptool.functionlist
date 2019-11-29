# Command line / stdio

## Example of status output

Step 1: Parsing all CrypTool files [ok]

Step 2: Parsing all CrypTool 2 files [ok]

Step 3: Parsing all JCrypTool files [error]: File not found: JCrypTool.csv

## Errors

- Stacktrace for errors that occur in own code and are anticipatable should result in a sentence output. A stack trace alone is not sufficient.
- Whether a stack trace is shown, should be configurable (dev mode)
- Crash = Program stops with any exception that was not caught. Interpreter or system acquits with stack trace or other means.
- Controlled error exit: Exception is caught at top level and processed. Program exits with nonzero status code.

Controlled error is the preferred means.

## Command line config

Negative example: 

- do_something -x pfad1 -y pfad2 -z option 1

Positive example:

- do something [-x pfad1] [-y pfad2]

where -x pfad 1 and -y pfad 2 are optional. Their default values are controlled by a config file. Preferrably, they are identified there as something like:

do_something.pfad1 = default1
do_something.pfad2 = default2
