# %%          IMPORTS
############# IMPORTS ##########################################################################################################

import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from clig import Arg, data

from .cellfuncs import (
    Cell,
    Notebook,
    __format_markdown_cell,
    __format_python_file_cell,
    __format_python_repl_snippet_cell,
    __format_shell_cell,
    __get_notebook_example_prefix,
    __is_python_file_code_cell,
    __is_python_repl_code_cell,
    __is_shell_command_code_cell,
)

# %%          PUBLIC FUNCTIONS
############# PUBLIC FUNCTIONS #################################################################################################


def nbmd(
    filepath: Arg[list[Path] | Path | None, data(nargs="*")] = None,
    kind: Literal["tutorial", "function", "class"] = "tutorial",
    prettier: bool = True,
):
    """Process jupyter nb files to generate markdown (md) files.

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of jupyter notebook (`.ipynb`) to convert do markdown.
        If `None`, process all notebook files from the current directory.

    - `kind` (`Literal["tutorial", "function", "class"]`, optional): Defaults to `"tutorial"`.
        The kind of the notebook files documentation to convert.

    - `prettier` (`bool`, optional): Defaults to `True`.
        Whether or not to pos process the generate md files with `prettier`, if prettier is available.

    """

    if kind != "tutorial":
        print("Not yet implemented")

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    for path in filepath:

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        lines: list[str] = []

        previous_was_simple_python_repl_snippet: bool = False
        for cell in notebook["cells"]:

            if cell["metadata"] and "to_hide" in cell["metadata"]["tags"]:
                continue

            if cell["cell_type"] == "markdown":
                lines.append(__format_markdown_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_shell_command_code_cell(cell):
                lines.append(__format_shell_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_python_file_code_cell(cell):
                lines.append(__format_python_file_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_python_repl_code_cell(cell):
                lines.append(__format_python_repl_snippet_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = True

        text: str = "".join(lines)

        markdown_filepath: Path = path.with_suffix(".md")

        with open(markdown_filepath, "w", encoding="utf-8") as file:
            file.write(text)

        if prettier:
            error_code = os.system("prettier --version")
            if error_code == 0:
                os.system(f"prettier --write {markdown_filepath}")
            else:
                print("No `prettier` command run")

        print(f"Processed file {markdown_filepath}")


def nbex(
    filepath: Arg[list[Path] | Path, data(nargs="*")],
    change_shell_cells: bool = False,
    output_suffix: str = "",
):

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    for path in filepath:

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        cells: list[Cell] = notebook["cells"]

        example_number: int = 0
        previous_example_prefix: str = __get_notebook_example_prefix(cells[:1])
        example_prefix = previous_example_prefix

        for i, cell in enumerate(cells):

            source: list[str] | None = cell.get("source")

            if __is_python_file_code_cell(cell):
                example_prefix: str = __get_notebook_example_prefix(cells[: i + 1])
                if example_prefix == previous_example_prefix:
                    example_number += 1
                else:
                    example_number = 1
                    previous_example_prefix = example_prefix

                example_filename: str = f"{example_prefix}{example_number:02d}.py"
                source[1] = f"# {example_filename}\n"

                with open(example_filename, "w", encoding="utf-8") as file:
                    file.write("".join(source[1:]))

            if change_shell_cells:
                if __is_shell_command_code_cell(cell):
                    if source[0].startswith("! python") and any([s.endswith(".py") for s in source[0].split()]):
                        parts: list[str] = source[0].split(".py")
                        parts[0] = f"! python {example_prefix}{example_number:02d}.py"
                        source[0] = "".join(parts)

            if source:
                cell["source"] = source  # update source
                cells[i] = cell  # update cell

        notebook["cells"] = cells
        if output_suffix:
            path: Path = path.with_suffix(f".{output_suffix}.ipynb")

        with open(path, "w", encoding="utf-8") as file:
            json.dump(notebook, file, indent=4)
