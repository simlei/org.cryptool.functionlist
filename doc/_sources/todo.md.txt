# TODO, shortcomings, Troubleshooting

see `https://github.com/simlei/org.cryptool.functionlist/issues`_ for documented problems and shortcomings, and workarounds.

- slightly different amount of entries between ./ws/{en,de}/scsv_webdump/{cto,ct1}.csv (Solution: not critical, static files, to be fixed by hand and kept that way)
- CT2 output is still erroneus: slight unsymmetricity between en,de files and ISO-8859-2 encoding) -- temporary solution: Use manually "repaired" files that are already in `./ws-static` and in effect in the `./config.yaml`
