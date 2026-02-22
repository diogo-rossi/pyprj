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

os.system(pyprj docs nbmd)

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
