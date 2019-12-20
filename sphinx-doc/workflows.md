# Workflows

The "**Main program step**" in each workflow marks the step which is to be performed successfully (and should be included in the step sequence with its dependencies in the `config.yaml`/command line arguments) for that workflow.

For an overview of how the steps work together by default, see [Steps Config and Data](config_data.md)

## Change files and test changes

**Main program step**: `step.tohtml_{de,en}` for testing, and its dependencies

Often, before releasing a new version of the functionality list to the website, the user would like to test if everything is in order with the manually-managed part of the [data sources](datasources.html).

- run `./src/flistapp.py` with the preconfigured configuration
- after the run completes without errors, check the HTML page `./ws/www/index.html` for an interactive (albeit mocked-up) version of the final result.
- change input files of the steps where necessary, repeat if necessary.

## Add category mappings for CT2 and JCT

**Main program step**: `step.categories_{ct2,jct}_{de,en}`

Categories are not generated by JCT and CT2 as these tools have no notion of this data. It is manually assigned to IDs of functionality in the steps `step.categories_{jct,ct2}_{en,de}`.

- The categories available are listed in ./ws/data/categories.csv. Only categories that are in this file can be assigned to csv rows.
- After running the program where it was detected that some categories are missing, the user is notified of it and asked to edit the file configured as `step.categories_{ct2,jct}_{en,de}.feedbackfile`
- These feedback files have placeholders where the user should enter the categories (always use the english version).
- re-run the program as before -- the categories from the feedback files are now integrated.

To consider:

- ca. 500 category mappings have been extracted from legacy data. The extracted mappings are the "trunk" input of the category database and resides in `step.categories_{ct2,jct}.input`.
- After the feedback file manual input has been verified to be correct, it should be cut and pasted at some time to the end of this "trunk" input filein `./ws` and more importantly, `./ws-static`, where it can be versioned by git and used as workspace template for other collaborators.

## Add functionality mappings for JCT

**Main program step**: `step.CT2scsv_{jct}_{de,en}`

The data necessary to group multiple functionalities under a common name is not provided by the JCT implementation. Thus, JCT entries are generated as each functionality being in its own group under its own name.


For now, this can be worked around by editing the input files for `step.CT2scsv_jct_{de,en}` by hand. This can then later be used to extract the manual work done via script and create the ID-to-functionality mapping as is practiced already with categories.

The structure of these files is as follows, on the english example:

```
[...]
Camellia192_CBC;[n.a.];
;[A];Block Ciphers \ Camellia \ Camellia192_CBC

Camellia128_CBC;[n.a.];
;[A];Block Ciphers \ Camellia \ Camellia128_CBC
[...]
```

English and German versions have to by symmetrical -- each line has to have the exact translated correspondence in the other file.

Following an empty line is the "Functionality group", followed by a semicolon, followed by a string that has to be there for legacy reasons, followed by a final semicolon. 
Then, without newlines, follow functionality addresses within the tool. Such a line has to start with a semicolon. Then, a single character in brackets indicates one of possibly many ways a tool offers functionalities. After another semicolon, backslash- or slash-separated path elements indicate a path the user has to follow (e.g. with mouse clicks in a menu) to reach the functionality.
The above example could be grouped like this:

```
[...]
Camellia;[n.a.];
;[A];Block Ciphers \ Camellia \ Camellia192_CBC
;[A];Block Ciphers \ Camellia \ Camellia128_CBC
[...]
```

... and accordingly, in the german file.

TODO: to be handled soon in the same way as the categories.

## Make changes permanent

The workspace folder is somewhat of a temporary state; it is target of temporary and user-feedback files. It's created initially as a clean copy of the `./ws-static` directory. It is also not tracked by version control, except for the `www` subdirectory (for convenience and simple web hosting).

This means, that git-revisionable, permanent user input (like category and functionality group inputs) should be made permanent by copying them over to `./ws-static` when the user is confident that the copied data is suitable.

## Update the website

**Main program step**: `step.tofinalform_{de,en}`

- The files configured as `step.tofinalform_{de,en}.output` are of a format that is suitable to be imported into the database of [cryptool.org](https://cryptool.org). Log into the [PHPMyAdmin](https://www.cryptool.org/restricted/phpmyadmin/) interface (credentials required, Webmaster: js {at} joerg {space} schneider {dot} com).
- Locate the databases "`j373_custom_cryptool_functions{de,en}`".
- In the upper navigation bar, select "Import"
- Choose CSV as import format, with semicolon delimiter (`;`)
- After a short while, the updated website should be available. Try Ctrl+F5 if it does not update.