# PyPrj

An opinionated CLI tool to manage python projects.

## Installation

```bash
pip install pyprj
```

## Usage

Look at the help messages from the CLI (pass `--help`). Some of the messages are
bellow.

### Main command

```sh
❯ pyprj --help
usage: pyprj [-h] {init,test,docs} ...

A CLI to manage python projects with predefined tools.

options:
  -h, --help        Show this help message and exit.

subcommands:
  {init,test,docs}
    init            Create a new project for a python package.
    test            Run task 'test' inside the project.
    docs            Manage documentation of the project.
```

### `init` subcommand

```sh
❯ pyprj init --help
usage: pyprj init [-h] [-p <python>] [-b <black-line-length>]

Create a new project for a python package.

options:
  -h, --help            Show this help message and exit.

  -p <python>, --python <python>
                        The Python interpreter to use to determine the minimum
                        supported Python version.
                        Defaults to '3.12'.

  -b <black-line-length>, --black-line-length <black-line-length>
                        Line length parameter to use with `black`.
                        Defaults to '128'.
```

### `test` subcommand

```sh
❯ pyprj test --help
usage: pyprj test [-h]

Run task 'test' inside the project.

This command only runs the task 'test' inside the project.
Tasks use the tool 'taskipy'. Currently are run with the tool 'uv.'
The task 'test' runs tests with 'pytest' in folder './tests'.

options:
  -h, --help  Show this help message and exit.
```

### `docs` subcommand

```sh
❯ pyprj docs --help
usage: pyprj docs [-h] {init,nbmd,nbex,modm} ...

Manage documentation of the project.

If called without subcommands, runs the task 'docs' inside the project.
Tasks use the tool 'taskipy'. Currently are run with the tool 'uv.'
The task 'docs' makes docs with 'sphinx' in folder './doc/sphinx'.

options:
  -h, --help            Show this help message and exit.

subcommands:
  {init,nbmd,nbex,modm}
    init                Initialize documentation folder with packages.
    nbmd                Process jupyter (nb) files to generate markdown (md) files.
    nbex                Process jupyter (nb) files to generate example files of code.
    modm                Process documentation in modules.
```

#### `docs/init` subcommand

```sh
❯ pyprj docs init --help
usage: pyprj docs init [-h]

Initialize documentation folder with packages.

options:
  -h, --help  Show this help message and exit.
```

#### `docs/nbmd` subcommand

```sh
❯ pyprj docs nbmd --help
usage: pyprj docs nbmd [-h] [-k {tutorial,function,class}] [-n] [-r <pattern>] [filepath ...]

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
```

#### `docs/nbex` subcommand

```sh
❯ pyprj docs nbex --help
usage: pyprj docs nbex [-h] [-c] [-d <dest-directory>] [-o <output-suffix>] [filepath ...]

Process jupyter (nb) files to generate example files of code,
creating files from the cells starting with '%%python'

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

#### `docs/modm` subcommand

```sh
❯ pyprj docs modm --help
usage: pyprj docs modm [-h] [filepath ...]

Process documentation in modules.

positional arguments:
  filepath    The filepath or filepaths of modules (.py) to process.
              If `None` (default), process all python files from the current directory.

options:
  -h, --help  Show this help message and exit.
```
