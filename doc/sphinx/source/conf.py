# %%          IMPORTS AND SETTINGS
############# IMPORTS AND SETTINGS #############################################################################################

import os
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

from sphinx.application import Sphinx

from pyprj import nbmd
from pyprj.markdown_utils import get_markdown_sections
from pyprj.pyproject import author_name, pkg_name, pkg_version, pyproject


class PyDomainInfo(TypedDict):
    module: str
    fullname: str


COLUMNS: int = 100
try:
    COLUMNS = os.get_terminal_size().columns
except OSError:
    pass
SEP: str = COLUMNS * "-"

THIS_DIR: Path = Path(__file__).parent.resolve()
os.chdir(THIS_DIR)

notebooks_dirpath: Path = Path("./notebooks")

nbmd.nbmd(notebooks_dirpath)

print(f"{SEP}\n> Preparing README")
index_sections: list[str] = get_markdown_sections(Path("index.md"))
usage_sections: list[str] = [
    f"#{sec}" if sec.startswith("#") else sec for sec in get_markdown_sections(notebooks_dirpath / "helps.md")
]

readme: str = "".join(index_sections[0:3]) + "".join(usage_sections)

with open(pyproject.dirpath / "README.md", "w", encoding="utf-8") as file:
    file.write(readme)

print(SEP)

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
myst_enable_extensions = [
    "dollarmath",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#math-shortcuts
    "amsmath",
    "html_image",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images
    "colon_fence",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons
]


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
