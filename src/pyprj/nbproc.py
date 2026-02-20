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


def nbmd(
    filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None,
    kind: Literal["tutorial", "function", "class"] = "tutorial",
    no_prettier: bool = False,
    remove_pattern_shell_files: Arg[str, data(metavar="<pattern>")] = "examples/",
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


def nbex(
    filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None,
    change_shell_cells: bool = False,
    dest_directory: Path = Path("examples/"),
    output_suffix: str = "",
):
    """Process jupyter (nb) files to generate example files of code,
    creating files from the cells starting with '%%python'

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of jupyter notebook (`.ipynb`) to
        generate examples. If `None` (default), process all notebook
        files from the current directory.

    - `change_shell_cells` (`bool`, optional): Defaults to `False`.
        Whether to edit the following shell cells, after the example cells.

    - `dest_directory` (`Path`, optional): Defaults to `Path("examples")`.
        Directory of the resulting examples files.

    - `output_suffix` (`str`, optional): Defaults to `""`.
        If editing original notebook file (`change_shell_cells=True`) add this
        suffix to the resulting file. Used for debbuging purposes, to not overwrite
        the original file (which is done with the default value).
    """

    dest_directory.mkdir(exist_ok=True)

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    if len(filepath) == 0:
        print("\nNo notebook files found.\n")
        return

    for path in filepath:

        print(f"> processing file: {path.as_posix()}")

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        cells: list[Cell] = notebook["cells"]

        example_number: int = 0
        previous_example_prefix: str = __get_notebook_example_prefix(cells[:1])
        example_prefix = previous_example_prefix
        example_filename: str = ""
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

                example_path: Path = dest_directory / example_filename
                print(f"    > generating example: {example_path.as_posix()}")
                with open(example_path, "w", encoding="utf-8") as file:
                    file.write("".join(source[1:]))

            if change_shell_cells:
                if __is_shell_command_code_cell(cell):
                    if source[0].startswith("! python") and any([s.endswith(".py") for s in source[0].split()]):
                        parts: list[str] = source[0].split(".py")
                        parts[0] = f"! python {dest_directory.as_posix()}/{example_filename}"
                        source[0] = "".join(parts)

            if source:
                cell["source"] = source  # update source
                cells[i] = cell  # update cell

        notebook["cells"] = cells
        if output_suffix:
            path: Path = path.with_suffix(f".{output_suffix}.ipynb")

        with open(path, "w", encoding="utf-8") as file:
            json.dump(notebook, file, indent=4)
