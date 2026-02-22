import sys
from typing import Literal

from clig import Arg, data

from .run_cmd import run_cmd
from .taskscmd import build as buill_project


def upver(semver: Arg[Literal["major", "minor", "patch"], data(nargs="?")], build: bool = False):
    """Update or show project version.

    Currently, it uses the command `uv version`.
    If called without positional arguments, only show the project version.

    Parameters
    ----------
    - `semver` (`Literal["major", "minor", "patch"]`, optional):.
        Semantic version pattern of the updated version.

    - `build` (`bool`, optional): Defaults to `False`.
        Whether to build the project after update version.
    """

    if not semver:
        error_code: int = run_cmd(f"uv version", kind="uv")
        if error_code != 0:
            sys.exit("\nNo `pyproject.toml` file found in this directory or parent directories.\nIt is not a project yet.\n")
        print(f"\nThe current pPackage is in this version")
        print("To update the project version, use positional arguments to `upver` subcommand.")
        print(" | ".join(["major", "minor", "patch"]))
        return error_code

    run_cmd(f"uv version --bump {semver}", kind="uv")

    if build:
        buill_project()
