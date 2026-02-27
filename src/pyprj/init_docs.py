import os
import shutil
import sys
from pathlib import Path

from .create_file_folder import __create_file, __create_folder
from .run_cmd import SEP, run_cmd
from .templates.ADVANCED_USE import ADVANCEDUSE
from .templates.APIREFERENCE import APIREFRENCE
from .templates.CONF import CONF_PY
from .templates.INDEX import INDEX_MD
from .templates.NBUSERGUIDE import NBUSERGUIDE

LOGO_PNG: Path = Path(__file__).parent.resolve() / "logo.png"

DOC_FOLDER: Path = Path("./doc")
SPHINX_SOURCE_FOLDER: Path = DOC_FOLDER / "sphinx/source"

TREE: str = f"""
```
    {DOC_FOLDER}
    │
    ├───icon
    │       logo.png
    │
    ├─── mkdocs
    └─── sphinx
        │   make.bat
        │   Makefile
        │
        ├─── build
        └───source
            │   advanceduse.md
            │   apireference.md
            │   conf.py
            │   index.md
            │
            ├───notebooks
            │   │   userguide.ipynb
            │   │
            │   └───examples
            ├───_static
            └───_templates
```
"""


def init(add_pyprj: bool = False):
    """Initialize documentation folder with packages.

    Parameters
    ----------
    - `add_pyprj` (`bool`, optional): Defaults to `False`.
        Whether to add `pyprj` itself in the `docs` dependency group of the project.
    """

    from .pyproject import author_name_url, documentation_page, pkg_name, pypi_project, source_repo

    doc_pkgs: list[str] = [
        "sphinx",
        "sphinx-copybutton",
        "sphinx-mathjax-offline",
        "sphinxnotes-comboroles",
        "myst-parser",
        "jupyter",
        "furo",
    ]
    if add_pyprj:
        doc_pkgs.append("pyprj")
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

    for folder in ["", "mkdocs", "sphinx", "icon"]:
        __create_folder(DOC_FOLDER / folder)

    print(SEP)
    print("Running Sphinx quick start in docs folder")
    cmd: str = (
        f"uv run sphinx-quickstart doc/sphinx --sep --project PROJECT --author AUTHOR --release RELEASE --language LANGUAGE"
    )
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    for folder in ["sphinx/source/notebooks", "sphinx/source/notebooks/examples"]:
        __create_folder(DOC_FOLDER / folder)

    msg: str = f"> editing file '{SPHINX_SOURCE_FOLDER.as_posix()}/conf.py'"
    print(f"{msg}")
    with open(SPHINX_SOURCE_FOLDER / "conf.py", "w", encoding="utf-8") as file:
        file.write(CONF_PY)

    __create_file(
        f"{SPHINX_SOURCE_FOLDER.as_posix()}/index.md",
        INDEX_MD.format(
            pkg_name=pkg_name,
            author_name=author_name_url,
            source_repo=source_repo,
            pypi_project=pypi_project,
            documentation_page=documentation_page,
        ),
    )
    __create_file(f"{SPHINX_SOURCE_FOLDER.as_posix()}/advanceduse.md", ADVANCEDUSE)
    __create_file(f"{SPHINX_SOURCE_FOLDER.as_posix()}/apireference.md", APIREFRENCE.replace("{{pkg_name}}", pkg_name))

    nbuserguide = (
        NBUSERGUIDE
        if add_pyprj
        else NBUSERGUIDE.replace(r'"%load_ext pyprj"', "").replace(r"%%writeexample", r"%%python -c \"\"")
    )
    __create_file(f"{SPHINX_SOURCE_FOLDER.as_posix()}/notebooks/userguide.ipynb", nbuserguide)

    msg: str = f"> creating file '{DOC_FOLDER.as_posix()}/icon/logo.png'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    shutil.copy(LOGO_PNG, DOC_FOLDER / "icon")

    msg: str = f"> removing file '{SPHINX_SOURCE_FOLDER.as_posix()}/index.rst'"
    sep: str = "-" * len(msg)
    print(f"{msg}")
    os.remove(SPHINX_SOURCE_FOLDER / "index.rst")

    print(f"{sep}")
    print(f"\nCreated subfolder '{DOC_FOLDER.as_posix()}' for documentation:")
    print(TREE.format(pkg_name=pkg_name))
    print("With the follwing packages in the `doc` dependency group:")
    print("- " + " | ".join(doc_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")
