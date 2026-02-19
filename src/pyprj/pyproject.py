import tomllib
from typing import TypedDict, cast


class Author(TypedDict):
    name: str
    email: str


class PyProjectData(TypedDict):
    name: str
    version: str
    authors: list[Author]


class PyProject(TypedDict):
    project: PyProjectData


with open("pyproject.toml", "rb") as f:
    pyproject = pyproject = cast(PyProject, tomllib.load(f))

pkg_name: str = pyproject["project"]["name"]
author_name: str = pyproject["project"]["authors"][0]["name"].replace(" ", "-").lower()
source_repo: str = f"https://github.com/{author_name}/{pkg_name}"
pypi_project: str = f"https://pypi.org/project/{pkg_name}/"
documentation_page: str = f"https://{pkg_name}.readthedocs.io/en/latest/"
