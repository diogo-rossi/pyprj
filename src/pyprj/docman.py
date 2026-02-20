import os
import shutil
import sys
from pathlib import Path
from typing import Any

from clig import Arg, Context, data

from .run_cmd import SEP, run_cmd
from .taskscmd import run_task

CONF_PY = r"""# %%          IMPORTS AND SETTINGS
############# IMPORTS AND SETTINGS #############################################################################################

import os
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict, cast


class PyDomainInfo(TypedDict):
    module: str
    fullname: str


class Author(TypedDict):
    name: str
    email: str


class PyProjectData(TypedDict):
    name: str
    version: str
    authors: list[Author]


class PyProject(TypedDict):
    project: PyProjectData


THIS_DIR: Path = Path(__file__).parent.resolve()
os.chdir(THIS_DIR)

ROOT_DIR = THIS_DIR.parent.parent.parent
PYPROJECT_TOML = ROOT_DIR / "pyproject.toml"

with open(PYPROJECT_TOML, "rb") as f:
    pyproject = cast(PyProject, tomllib.load(f))

project_data: PyProjectData = pyproject["project"]
project_name = project_data["name"]
project_author = project_data["authors"][0]["name"]


# %%          SPHINX DATA
############# SPHINX DATA ######################################################################################################

project = project_name
copyright = f"{datetime.now().year}, {project_author}"
author = project_author
release = project_data["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinxnotes.comboroles",
    "sphinx.ext.linkcode",
]

templates_path = ["_templates"]
exclude_patterns = []

maximum_signature_line_length = 70
napoleon_google_docstring = True
napoleon_numpy_docstring = False
default_role = "code"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

html_theme = "furo"
html_title = f'<p style="text-align: center"><b>{project_name}</b></p>'
html_css_files = ["css/custom.css"]
html_logo = "../../logo.png"
myst_heading_anchors = 4


def linkcode_resolve(domain: Literal["py", "c", "cpp", "javascript"], info: PyDomainInfo) -> str:
    return "test"
"""

INDEX_MD = """# {pkg_name}

Description of the project.

## Installation

```bash
pip install {pkg_name}
```

```{{toctree}}
:caption: Table of contents
:maxdepth: 1

userguide
apireference
```

## Links

- Source repository:
  [{source_repo}]({source_repo})
- PyPI:
  [{pypi_project}]({pypi_project})
- Documentation:
  [{documentation_page}]({documentation_page})
"""

LOGO_PNG: Path = Path(__file__).parent.resolve() / "logo.png"

DOC_FOLDER: Path = Path("./doc")
SPHINX_SOURCE_FOLDER: Path = DOC_FOLDER / "sphinx/source"

TREE: str = f"""
```
    {DOC_FOLDER}
    │    logo.png
    │
    ├─── mkdocs
    └─── sphinx
        │   make.bat
        │   Makefile
        │
        ├─── build
        └─── source
            │   conf.py
            │   index.md
            │   userguide.md
            │   apireference.md
            │
            ├─── _static
            ├─── _templates
            └─── notebooks
                 └─── examples
```
"""


def docs(ctx: Context):
    """Manage documentation of the project.

    If called without subcommands, runs the task 'docs' inside the project.
    Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
    The task 'docs' makes docs with 'sphinx' in folder './doc/sphinx'.
    """
    if vars(ctx.namespace)[ctx.command.sub_commands["docs"].subparsers_dest] is None:
        run_task("docs")


def init():
    """Initialize documentation folder with packages."""

    from .pyproject import author_name_url, documentation_page, pkg_name, pypi_project, source_repo

    doc_pkgs: list[str] = ["sphinx", "sphinx-copybutton", "sphinxnotes-comboroles", "myst-parser", "jupyter", "furo"]
    cmd: str = f"uv add --group docs {' '.join(doc_pkgs)}"

    print(f"{SEP}\nAdding 'docs' packages")
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    cmd: str = "uv sync --all-groups"
    print(f"{SEP}\nSyncing packages")
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    for folder in ["", "mkdocs", "sphinx"]:
        folder_path: Path = DOC_FOLDER / folder
        msg: str = f"> creating folder '{folder_path.as_posix()}'"
        print(f"{msg}")
        try:
            os.mkdir(folder_path)
        except:
            print(f"{SEP}")
            raise

    print(SEP)
    print("Running Sphinx quick start in docs folder")
    cmd: str = (
        f"uv run sphinx-quickstart doc/sphinx --sep --project PROJECT --author AUTHOR --release RELEASE --language LANGUAGE"
    )
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    for folder in ["sphinx/source/notebooks", "sphinx/source/notebooks/examples"]:
        folder_path: Path = DOC_FOLDER / folder
        msg: str = f"> creating folder '{folder_path.as_posix()}'"
        print(f"{msg}")
        try:
            os.mkdir(folder_path)
        except:
            print(f"{SEP}")
            raise

    msg: str = f"> editing file '{SPHINX_SOURCE_FOLDER.as_posix()}/conf.py'"
    print(f"{msg}")
    with open(SPHINX_SOURCE_FOLDER / "conf.py", "w", encoding="utf-8") as file:
        file.write(CONF_PY)

    msg: str = f"> creating file '{SPHINX_SOURCE_FOLDER.as_posix()}/index.md'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    with open(SPHINX_SOURCE_FOLDER / "index.md", "w", encoding="utf-8") as file:
        file.write(
            INDEX_MD.format(
                pkg_name=pkg_name,
                author_name=author_name_url,
                source_repo=source_repo,
                pypi_project=pypi_project,
                documentation_page=documentation_page,
            )
        )

    msg: str = f"> creating file '{SPHINX_SOURCE_FOLDER.as_posix()}/userguide.md'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    with open(SPHINX_SOURCE_FOLDER / "userguide.md", "w", encoding="utf-8") as file:
        file.write("# User guide")

    msg: str = f"> creating file '{SPHINX_SOURCE_FOLDER.as_posix()}/apireference.md'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    with open(SPHINX_SOURCE_FOLDER / "apireference.md", "w", encoding="utf-8") as file:
        file.write("# API reference")

    msg: str = f"> creating file '{DOC_FOLDER.as_posix()}/logo.png'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    shutil.copy(LOGO_PNG, DOC_FOLDER)

    msg: str = f"> removing file '{SPHINX_SOURCE_FOLDER.as_posix()}/index.rst'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    os.remove(SPHINX_SOURCE_FOLDER / "index.rst")

    print(f"{sep}")
    print(f"\nCreated subfolder '{DOC_FOLDER.as_posix()}' for documentation:")
    print(TREE.format(pkg_name=pkg_name))
    print("With the follwing packages in the `doc` dependency group:")
    print("- " + " ".join(doc_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")


def modm(filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None):
    """Process documentation in modules.

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of modules (.py) to process.
        If `None` (default), process all python files from the current directory.
    """
    print("\nTODO: not yet implemented!\n")
