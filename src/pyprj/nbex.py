import json
from collections.abc import Iterable
from pathlib import Path

from clig import Arg, data

from .cellfuncs import (
    Cell,
    Notebook,
    __get_notebook_example_prefix,
    __is_python_file_code_cell,
    __is_shell_command_code_cell,
    _generate_example,
)


def nbex(
    filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None,
    only_rename_examples: bool = False,
    no_change_shell_cells: bool = False,
    dest_directory: Path = Path("examples/"),
    output_suffix: str = "",
):
    """Process jupyter (nb) files to generate example files of code.
    Create files from the cells starting with `%%`.

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of jupyter notebook (`.ipynb`) to
        generate examples. If `None` (default), process all notebook
        files from the current directory.

    - `only_rename_examples` (`bool`, optional): Defaults to `False`.
        Whether to only rename the example cells, not generating example files.

    - `no_change_shell_cells` (`bool`, optional): Defaults to `False`.
        Whether to not edit the following shell cells, after the example cells.

    - `dest_directory` (`Path`, optional): Defaults to `Path("examples")`.
        Directory of the resulting examples files.

    - `output_suffix` (`str`, optional): Defaults to `""`.
        If editing original notebook file (`change_shell_cells=True`) add this
        suffix to the resulting file. Used for debbuging purposes, to not overwrite
        the original file (which is done with the default value).
    """

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    if len(filepath) == 0:
        print("\nNo notebook files found.\n")
        return

    files_in_folders = []
    for path in filepath[:]:
        if path.is_dir():
            files_in_folders.extend(list(path.glob("*.ipynb")))
            filepath.remove(path)
    filepath.extend(files_in_folders)

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

                if not only_rename_examples:
                    file_dest_dir: Path = path.parent / dest_directory
                    file_dest_dir.mkdir(exist_ok=True)
                    _generate_example(source[1:], example_filename, file_dest_dir)

            if not no_change_shell_cells:
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
