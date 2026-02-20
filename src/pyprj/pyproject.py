import tomllib
from pathlib import Path
from typing import TypedDict, cast

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


pyproject: PyProject = PyProject(Path(".").resolve())

pyproject_filepath: Path = pyproject.dirpath / "pyproject.toml"

with open(pyproject_filepath, "rb") as f:
    pyproject_dict = cast(PyProjectDict, tomllib.load(f))


pkg_name: str = pyproject_dict["project"]["name"]
version: str = pyproject_dict["project"]["version"]
author_name: str = pyproject_dict["project"]["authors"][0]["name"].replace(" ", "-").lower()
source_repo: str = f"https://github.com/{author_name}/{pkg_name}"
pypi_project: str = f"https://pypi.org/project/{pkg_name}/"
documentation_page: str = f"https://{pkg_name}.readthedocs.io/en/latest/"
