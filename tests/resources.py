import json
from pathlib import Path

from pyprj.cellfuncs import Notebook

THIS_DIR = Path(__file__).parent

notebook_filepath: Path = THIS_DIR / "notebooks" / "notebookexample.ipynb"
with open(notebook_filepath, "r", encoding="utf-8") as file:
    notebook: Notebook = json.load(file)

cells = notebook["cells"]
