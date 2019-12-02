# Zusammengefasst, für Gespräch

## Goals achieved @ 2019-12-01 19:00 PM

- [x] correct steps to run
- [x] Python version documented
- [ ] (only minimally) code documentation
- [x] Robustness, logging, top-level processing of exceptions (project-space vs library exceptions)
- [x] Logging into console
- [x] user documentation (shifting still, e.g. file locations may be incorrect. Mostly there, though)
- [x] top-level config file
- [x] script that runs the whole process (for users)

## In preparation for talking about it

- The main, default entry point for running it is `bin/flist.py` without arguments. Accepts `--workspace`.
- The main, default entry point for configuration is `config.yaml`
- The main entry point for web documentation is https://github.com/simlei/org.cryptool.functionlist/
- Check out \${workspace}/html after a full run :)

- documentation of the code is lacking due to not getting everything quite done in the allotted time

## TODO next

- [x] merged CSV is websitetauglich: höchstwahrscheinlich, Test bleibt aus (aber lokal kann die Website generiert werden und funktioniert gut)
- [x] ~~CT2 daten sind immer noch die statischen von der Website (wird sich heute aber ändern, Quelle ist dann ein per Hand eingefügter CT2 output)~~
- [ ] Kategorien sind bisher handgepflegt. zB, CT2 und JCT liefern keine Kategorien wie 1) Moder Ciphers mit
    - auch die müssen noch übersetzt werden.
- [ ] JCT dynamischer Output
- [ ] Übersetzung in Deutsch (CT/JCT Änderungen nötig davor). Davor: dump der phpMyAdmin Datenbank wird verwendet (mein Repo liefert es bis Montag mit)

Basiert auf Mail vom Fr. 29.11.: https://github.com/simlei/org.cryptool.functionlist/tree/00b03f553ebf00f28470bb80586c569f8d500ef0#todo-next
