# %%          IMPORTS
############# IMPORTS ##########################################################################################################

from typing import Literal, TypedDict

# %%          CLASSES
############# CLASSES ##########################################################################################################

Data = TypedDict("Data", {"text/plain": list[str]})


class Output(TypedDict):
    name: str
    output_type: Literal["stream", "execute_result"]
    text: list[str]
    data: Data


class MetaData(TypedDict):
    tags: list[str]


class Cell(TypedDict):
    cell_type: Literal["markdown", "code"]
    source: list[str]
    metadata: MetaData
    outputs: list[Output]


class Notebook(TypedDict):
    cells: list[Cell]


# %%          PRIVATE FUNCTIONS
############# PRIVATE FUNCTIONS ################################################################################################


def __end_snippet(previous_was_snippet: bool):
    return "```\n" if previous_was_snippet else ""


def __get_outputs(cell: Cell) -> str:

    if __is_python_file_code_cell(cell):
        return ""

    lines = []
    for o in cell["outputs"]:
        if o["output_type"] == "stream":
            lines.append("".join(o["text"]))
        if o["output_type"] == "execute_result":
            lines.append("".join(o["data"]["text/plain"]))
    out = "".join(lines)
    if "Traceback " in out:
        out = cell["outputs"][-1]["text"][-1]

    return out.strip() + "\n" if out else ""


def __format_markdown_cell(cell: Cell, previous_was_snippet: bool) -> str:
    out = __end_snippet(previous_was_snippet) + "".join(cell["source"])
    return out.strip() + "\n\n"


def __format_python_file_cell(cell: Cell, previous_was_snippet: bool):
    return __end_snippet(previous_was_snippet) + "```python\n" + "".join(cell["source"][1:]) + "\n```\n"


def __format_shell_cell(cell: Cell, previous_was_snippet: bool):
    return (
        (__end_snippet(previous_was_snippet))
        + ("```\n>" + cell["source"][0].lstrip("!"))
        + "\n\n"
        + __get_outputs(cell)
        + "```\n"
    )


def __format_python_repl_snippet_cell(cell: Cell, previous_was_snippet: bool):
    lines: list[str] = []
    for line in cell["source"]:
        lines.append(f"... {line}" if (line.startswith(" ") or len(line.strip()) == 0) else f">>> {line}")
    lines = [line for line in lines if ">>> pass" not in line]
    content = ("" if previous_was_snippet else "```python\n") + "".join(lines)
    return content.strip() + "\n" + __get_outputs(cell)


def __is_code_cell_with_source_content(cell: Cell) -> bool:
    return cell["cell_type"] == "code" and len(cell["source"]) > 0


def __is_code_cell_starting_with(cell: Cell, char: str) -> bool:
    return __is_code_cell_with_source_content(cell) and cell["source"][0].startswith(char)


def __is_shell_command_code_cell(cell: Cell) -> bool:
    return __is_code_cell_starting_with(cell, "!")


def __is_python_file_code_cell(cell: Cell) -> bool:
    return __is_code_cell_starting_with(cell, "%%") and cell["source"][1].startswith("#")


def __is_python_repl_code_cell(cell: Cell) -> bool:
    return __is_code_cell_with_source_content(cell) and not any(
        [__is_shell_command_code_cell(cell), __is_python_file_code_cell(cell)]
    )


def __get_notebook_example_prefix(cells: list[Cell]) -> str:
    for cell in reversed(cells):
        if cell["metadata"]:
            for tag in cell["metadata"]["tags"]:
                if tag.startswith("ex_"):
                    return tag.removeprefix("ex_")
    return "example"
