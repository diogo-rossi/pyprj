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

os.system("pyprj docs nbmd notebooks") # convert files inside 'notebooks/' folder

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

myst_heading_anchors = 4
myst_enable_extensions = [
    "dollarmath",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#math-shortcuts
    "amsmath",
    "html_image",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images
    "colon_fence",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

html_theme = "furo"
html_title = f'<p style="text-align: center"><b>{project_name}</b></p>'
html_css_files = ["css/custom.css"]
html_logo = "../../icon/logo.png"


def linkcode_resolve(domain: Literal["py", "c", "cpp", "javascript"], info: PyDomainInfo) -> str:
    return "test"


def convert_admonitions_to_myst(app, filename, lines: list[str]):
    _GITHUB_ADMONITIONS = {
        "> [!NOTE]": "note",
        "> [!TIP]": "tip",
        "> [!IMPORTANT]": "important",
        "> [!WARNING]": "warning",
        "> [!CAUTION]": "caution",
    }

    # loop through lines, replace github admonitions
    for i, orig_line in enumerate(lines):
        orig_line_splits = orig_line.split("\n")
        replacing = False
        for j, line in enumerate(orig_line_splits):
            # look for admonition key
            for admonition_key in _GITHUB_ADMONITIONS:
                if admonition_key in line:
                    line = line.replace(admonition_key, "```{" + _GITHUB_ADMONITIONS[admonition_key] + "}\n")
                    # start replacing quotes in subsequent lines
                    replacing = True
                    break
            else:
                # replace indent to match directive
                if replacing and "> " in line:
                    line = line.replace("> ", "  ")
                elif replacing:
                    # missing "> ", so stop replacing and terminate directive
                    line = f"\n```\n{line}"
                    replacing = False
            # swap line back in splits
            orig_line_splits[j] = line
        # swap line back in original
        lines[i] = "\n".join(orig_line_splits)


def setup(app: Sphinx):
    print(SEP)
    print("> Converting admonitions to MyST format")
    app.connect("source-read", convert_admonitions_to_myst)
    print("> Adding custom CSS file")
    app.add_css_file("custom.css")
    print(SEP)
"""
