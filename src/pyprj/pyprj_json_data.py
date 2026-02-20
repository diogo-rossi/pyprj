import json
from pathlib import Path
from typing import TypedDict

from .pyproject import pyproject


class PyPrjJSON(TypedDict):
    token: str
    published_versions: list[str]


pyprj_json_path: Path = pyproject.dirpath / ".vscode/pyprj.json"


with open(pyprj_json_path, "r", encoding="utf-8") as file:
    json_content: PyPrjJSON = json.load(file)

token: str = json_content["token"]
published_versions: list[str] = json_content["published_versions"]


def save_content(content: PyPrjJSON) -> None:
    with open(pyprj_json_path, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)
