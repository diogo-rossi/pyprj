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

pkg_name = pyproject["project"]["name"]
author_name = pyproject["project"]["authors"][0]["name"].replace(" ", "-").lower()
