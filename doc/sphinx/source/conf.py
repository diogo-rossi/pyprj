# %%          IMPORTS AND SETTINGS
############# IMPORTS AND SETTINGS #############################################################################################

import os
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

from pyprj import nbmd
from pyprj.markdown_utils import get_markdown_sections
from pyprj.pyproject import author_name, pkg_name, pkg_version, pyproject


class PyDomainInfo(TypedDict):
    module: str
    fullname: str


THIS_DIR: Path = Path(__file__).parent.resolve()
os.chdir(THIS_DIR)

notebooks_dirpath: Path = Path("./notebooks")

nbmd.nbmd(notebooks_dirpath)

index_sections: list[str] = get_markdown_sections(Path("index.md"))
usage_sections: list[str] = [
    f"#{sec}" if sec.startswith("#") else sec for sec in get_markdown_sections(notebooks_dirpath / "helps.md")
]

readme: str = "".join(index_sections[0:3]) + "".join(usage_sections)

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

myst_heading_anchors = 4


maximum_signature_line_length = 70
napoleon_google_docstring = True
napoleon_numpy_docstring = False
default_role = "code"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]
html_theme = "furo"
html_title = f'<p style="text-align: center"><b>{pkg_name}</b></p>'
html_css_files = ["css/custom.css"]
html_logo = "../../icon/logo.png"


def linkcode_resolve(domain: Literal["py", "c", "cpp", "javascript"], info: PyDomainInfo) -> str:
    return "test"
