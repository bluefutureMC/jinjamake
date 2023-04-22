# Jinja-Make
*jinjamake* is a simple jinja2 rendering script for multi-file projects.

The script takes all files from the CWD and it's subdirs that end with .j2, renders them using the given json data file, 
and writes them back to an `out` directory - keeping the same file structure as the they had relative to the CWD.

The recommended project file structure is as follows:
```
<root>
|
|- out
|  |
|  |- (rendered project files)
|
|- src
|  |
|  |- (template files ending with .j2)
|
|- lib
|  |
|  |- (macro library files ending with .macro)
|
|- globals.json
```

## Credits
This project uses the [Jinja2](https://pypi.org/project/Jinja2/) library to render template files.
For documentation on syntax and usage go to [jinja on palletsprojects](https://jinja.palletsprojects.com/).

This script is heavly inspired by [jinja2-cli](https://github.com/mattrobenolt/jinja2-cli)