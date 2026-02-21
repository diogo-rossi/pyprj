# %%          IMPORTS AND SETTINGS
############# IMPORTS AND SETTINGS #############################################################################################

import os
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

from pyprj import nbproc
from pyprj.pyproject import author_name, pkg_name, pkg_version, pyproject


class PyDomainInfo(TypedDict):
    module: str
    fullname: str


THIS_DIR: Path = Path(__file__).parent.resolve()
os.chdir(THIS_DIR)

notebooks_dirpath: Path = Path("./notebooks")

nbproc.nbmd(notebooks_dirpath)

with open(notebooks_dirpath / "helps.md", "r", encoding="utf-8") as file:
    readme: str = file.read()

with open(pyproject.dirpath / "README.md", "w", encoding="utf-8") as file:
    file.write(readme)

# %%          SPHINX DATA
############# SPHINX DATA ######################################################################################################

project = pkg_name
copyright = f"{datetime.now().year}, {author_name}"
author = author_name
release = pkg_version

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
html_title = f'<p style="text-align: center"><b>{pkg_name}</b></p>'
html_css_files = ["css/custom.css"]
html_logo = "../../logo.png"
myst_heading_anchors = 4


def linkcode_resolve(domain: Literal["py", "c", "cpp", "javascript"], info: PyDomainInfo) -> str:
    return "test"
