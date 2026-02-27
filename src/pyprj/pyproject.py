import sys
import tomllib
from pathlib import Path
from typing import TypedDict, cast

from taskipy.exceptions import MissingPyProjectFileError
from taskipy.pyproject import PyProject


class Author(TypedDict):
    name: str
    email: str


class ProjectData(TypedDict):
    name: str
    version: str
    authors: list[Author]


class PyProjectDict(TypedDict):
    project: ProjectData


try:
    pyproject: PyProject = PyProject(Path(".").resolve())
except MissingPyProjectFileError:
    sys.exit("\nNo 'pyproject.toml' file found in this directory or parent directories.\nIt is not a project yet.\n")

pyproject_filepath: Path = pyproject.dirpath / "pyproject.toml"


def __get_pyproject_data() -> PyProjectDict:
    with open(pyproject_filepath, "rb") as f:
        obj = cast(PyProjectDict, tomllib.load(f))
    return obj


pyproject_dict = __get_pyproject_data()

author_name: str = pyproject_dict["project"]["authors"][0]["name"]
author_email: str = pyproject_dict["project"]["authors"][0]["email"]

pkg_name: str = pyproject_dict["project"]["name"]
pkg_version: str = pyproject_dict["project"]["version"]
author_name_url: str = pyproject_dict["project"]["authors"][0]["name"].replace(" ", "-").lower()
source_repo: str = f"https://github.com/{author_name_url}/{pkg_name}"
pypi_project: str = f"https://pypi.org/project/{pkg_name}/"
documentation_page: str = f"https://{pkg_name}.readthedocs.io/en/latest/"
