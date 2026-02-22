import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from clig import Arg, data

from .cellfuncs import (
    Notebook,
    __format_markdown_cell,
    __format_python_file_cell,
    __format_python_repl_snippet_cell,
    __format_shell_cell,
    __is_python_file_code_cell,
    __is_python_repl_code_cell,
    __is_shell_command_code_cell,
)
from .run_cmd import run_cmd


def nbmd(
    filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None,
    kind: Literal["tutorial", "function", "class"] = "tutorial",
    no_prettier: bool = False,
    remove_pattern_shell_files: Arg[str, data(metavar="<pattern>")] = "examples/",
    dont_run_notebooks_before: bool = False,
):
    """Process jupyter (nb) files to generate markdown (md) files.

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of jupyter notebook (`.ipynb`) to convert
        to markdown. If `None` (default), process all notebook files from
        the current directory.

    - `kind` (`Literal["tutorial", "function", "class"]`, optional): Defaults to `"tutorial"`.
        The kind of the notebook files documentation to convert.

    - `no_prettier` (`bool`, optional): Defaults to `False`.
        Whether to not pos-process the generate .md files with 'prettier', if 'prettier' is available.

    - `remove_pattern_shell_files` (`str`, optional): Defaults to `"examples/"`.
        Pattern to remove in shell command line cells. Aiming to remove example command line folders from path.

    - `dont_run_notebooks_before` (`bool`, optional): Defaults to `False`.
        Whether to not run the jupyter notebooks before processing.
    """
    if kind != "tutorial":
        print("\nNot yet implemented. Currently, only 'kind=tutorial' is accepted.\n")
        return

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    for path in filepath[:]:
        if path.is_dir():
            filepath.remove(path)
            filepath.extend(path.glob("*.ipynb"))

    if len(filepath) == 0:
        print("\nNo notebook files found.\n")
        return

    print()
    prettier: bool = not no_prettier
    if prettier:
        print("> checking `prettier` version:")
        error_code = os.system("prettier --version")
        if error_code != 0:
            print("> No valid `prettier` command found")
            prettier = False
        print()

    for path in filepath:

        if not dont_run_notebooks_before:
            run_cmd(f"uv run jupyter nbconvert --to notebook --execute --inplace {path}", kind="uv")

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        lines: list[str] = []

        previous_was_simple_python_repl_snippet: bool = False
        for cell in notebook["cells"]:

            if cell["metadata"] and "tags" in cell["metadata"] and "to_hide" in cell["metadata"]["tags"]:
                continue

            if cell["cell_type"] == "markdown":
                lines.append(__format_markdown_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_shell_command_code_cell(cell):
                lines.append(__format_shell_cell(cell, previous_was_simple_python_repl_snippet, remove_pattern_shell_files))
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
            os.system(f"prettier --write {markdown_filepath}")

        print(f"> generated markdown file '{markdown_filepath}'\n")
