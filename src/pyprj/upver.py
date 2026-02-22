from typing import Literal

from clig import Arg, data

from .run_cmd import run_cmd


def upver(semver_part: Arg[Literal["major", "minor", "patch"], data(nargs="?")]):
    """Update or show project version.

    Currently, it uses the command 'uv version'.
    If called without positional arguments, only show the project version.
    """
    if not semver_part:
        error_code: int = run_cmd(f"uv version", kind="uv")
        if error_code != 0:
            sys.exit("\nNo 'pyproject.toml' file found in this directory or parent directories.\nIt is not a project yet.\n")
        print(f"\nThe current pPackage is in this version")
        print("To update the project version, use positional arguments to 'upver' subcommand.")
        print(" | ".join(["major", "minor", "patch"]))

    run_cmd(f"uv version --bump {semver_part}", kind="uv")
