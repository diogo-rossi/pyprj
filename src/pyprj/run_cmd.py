import os

from .printcolor import Color, printcolor

COLUMNS = 50
try:
    COLUMNS = os.get_terminal_size().columns
except OSError:
    pass


SEP: str = "-" * COLUMNS


def run_cmd(cmd: str, kind: str | None = None, add_sep: bool = True):

    cmdkind: str = f"`{kind}` " if kind else ""
    msg: str = f"> running {cmdkind}command: `{cmd}`"

    if "--token" in msg:
        msg = f"{msg.split("--token")[0]} --token *****"
        from .pyproject import pyproject

        pyproject_dirpath = pyproject.dirpath.as_posix()
        if pyproject_dirpath in msg:
            msg = msg.replace(pyproject_dirpath, ".")

    sep: str = "-" * len(msg)
    if add_sep:
        printcolor(f"{SEP}", Color.GREEN)
    printcolor(f"{msg}\n{sep}", Color.BLUE)
    error_code = os.system(cmd)
    printcolor(SEP, Color.GREEN)
    return error_code
