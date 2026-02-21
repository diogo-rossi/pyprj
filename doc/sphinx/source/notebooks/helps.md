# Usage

Look at the help messages from the CLI (using `--help`). Some of the messages
are bellow.

## Main command

```none
> pyprj --help

usage: pyprj [-h] [-v] {init,test,docs,build,version,publish} ...

A CLI to manage python projects with predefined tools.

options:
  -h, --help            Show this help message and exit.
  -v, --version         show program's version number and exit

subcommands:
  {init,test,docs,build,version,publish}
    init                Create a new project for a python package.
    test                Run task 'test' inside the project.
    docs                Manage documentation of the project.
    build               Run task 'build' inside the project.
    version             Update or show project version.
    publish             Publish package to PyPI.
```

## `init` subcommand

```none
> pyprj init --help

usage: pyprj init [-h] [-n <name>] [-p <python-version>] [-b <black-line-length>]

Create a new project for a python package.

options:
  -h, --help            Show this help message and exit.

  -n <name>, --name <name>
                        The name of the project. If `None`, use the current
                        directory's name.
                        Defaults to 'None'.

  -p <python-version>, --python-version <python-version>
                        The Python interpreter version to use to determine the
                        minimum supported Python version.
                        Defaults to '3.12'.

  -b <black-line-length>, --black-line-length <black-line-length>
                        Line length parameter to use with `black`.
                        Defaults to '128'.
```

## `test` subcommand

```none
> pyprj test --help

usage: pyprj test [-h]

Run task 'test' inside the project.

This command only runs the task 'test' inside the project.
Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
The task 'test' runs tests with 'pytest' in folder './tests'.

options:
  -h, --help  Show this help message and exit.
```

## `docs` subcommand

```none
> pyprj docs --help

usage: pyprj docs [-h] {init,nbex,nbmd,modm} ...

Manage documentation of the project.

If called without subcommands, runs the task 'docs' inside the project.
Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
The task 'docs' makes docs with 'sphinx' in folder './doc/sphinx'.

options:
  -h, --help            Show this help message and exit.

subcommands:
  {init,nbex,nbmd,modm}
    init                Initialize documentation folder with packages.
    nbex                Process jupyter (nb) files to generate example files of code.
    nbmd                Process jupyter (nb) files to generate markdown (md) files.
    modm                Process documentation in modules.
```

### `docs/init` subcommand

```none
> pyprj docs init --help

usage: pyprj docs init [-h]

Initialize documentation folder with packages.

options:
  -h, --help  Show this help message and exit.
```

### `docs/nbmd` subcommand

```none
> pyprj docs nbmd --help

usage: pyprj docs nbmd [-h] [-k {tutorial,function,class}] [-n] [-r <pattern>] [-d] [filepath ...]

Process jupyter (nb) files to generate markdown (md) files.

positional arguments:
  filepath              The filepath or filepaths of jupyter notebook (`.ipynb`) to convert
                        to markdown. If `None` (default), process all notebook files from
                        the current directory.

options:
  -h, --help            Show this help message and exit.

  -k {tutorial,function,class}, --kind {tutorial,function,class}
                        The kind of the notebook files documentation to convert.
                        Defaults to 'tutorial'.

  -n, --no-prettier     Whether to not pos-process the generate .md files with
                        'prettier', if 'prettier' is available.
                        Defaults to 'False'.

  -r <pattern>, --remove-pattern-shell-files <pattern>
                        Pattern to remove in shell command line cells. Aiming to
                        remove example command line folders from path.
                        Defaults to 'examples/'.

  -d, --dont-run-notebooks-before
                        Whether to not run the jupyter notebooks before
                        processing.
                        Defaults to 'False'.
```

### `docs/nbex` subcommand

```none
> pyprj docs nbex --help

usage: pyprj docs nbex [-h] [-c] [-d <dest-directory>] [-o <output-suffix>] [filepath ...]

Process jupyter (nb) files to generate example files of code.
Create files from the cells starting with '%%python'.

positional arguments:
  filepath              The filepath or filepaths of jupyter notebook (`.ipynb`) to
                        generate examples. If `None` (default), process all notebook
                        files from the current directory.

options:
  -h, --help            Show this help message and exit.

  -c, --change-shell-cells
                        Whether to edit the following shell cells, after the
                        example cells.
                        Defaults to 'False'.

  -d <dest-directory>, --dest-directory <dest-directory>
                        Directory of the resulting examples files.
                        Defaults to 'examples'.

  -o <output-suffix>, --output-suffix <output-suffix>
                        If editing original notebook file
                        (`change_shell_cells=True`) add this
                        suffix to the resulting file. Used for debbuging
                        purposes, to not overwrite
                        the original file (which is done with the default
                        value).
                        Defaults to ''.
```

### `docs/modm` subcommand

```none
> pyprj docs modm --help

usage: pyprj docs modm [-h] [filepath ...]

Process documentation in modules.

positional arguments:
  filepath    The filepath or filepaths of modules (.py) to process.
              If `None` (default), process all python files from the current directory.

options:
  -h, --help  Show this help message and exit.
```

## `build` subcommand

```none
> pyprj build --help

usage: pyprj build [-h]

Run task 'build' inside the project.

This command only runs the task 'build' inside the project.
Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
The task 'build' builds the package with 'uv' in root folder.

options:
  -h, --help  Show this help message and exit.
```

## `version` subcommand

```none
> pyprj version --help

usage: pyprj version [-h] [{major,minor,patch}]

Update or show project version.

If called without positional arguments, only show the project version.

positional arguments:
  {major,minor,patch}

options:
  -h, --help           Show this help message and exit.
```

## `publish` subcommand

```none
> pyprj publish --help

usage: pyprj publish [-h]

Publish package to PyPI.

Uses token from file '.vscode/pyprj.json'

options:
  -h, --help  Show this help message and exit.
```
