import os

from .pyproject import pyproject

COLUMNS = 50
try:
    COLUMNS = os.get_terminal_size().columns
except OSError:
    pass


SEP: str = "-" * COLUMNS
pyproject_dirpath = pyproject.dirpath.as_posix()


def run_cmd(cmd: str, kind: str | None = None, add_sep: bool = True):
    cmdkind: str = f"`{kind}` " if kind else ""
    msg: str = f"> running {cmdkind}command: `{cmd}`"

    if "--token" in msg:
        msg = f"{msg.split("--token")[0]} --token *****"

    if pyproject_dirpath in msg:
        msg = msg.replace(pyproject_dirpath, ".")

    sep: str = "-" * len(msg)
    if add_sep:
        print(f"{SEP}")
    print(f"{msg}\n{sep}")
    error_code = os.system(cmd)
    print(SEP)
    return error_code
