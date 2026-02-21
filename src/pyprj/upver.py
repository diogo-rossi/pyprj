from typing import Literal

from clig import Arg, data

from .run_cmd import run_cmd


def upver(semver_part: Arg[Literal["major", "minor", "patch"], data(nargs="?")]):
    """Update or show project version.

    If called without positional arguments, only show the project version.
    """
    if not semver_part:
        from .pyproject import pkg_name, pkg_version

        print(f"\nThe Package '{pkg_name}' is in version: {pkg_version}")
        print("To update the project version, use positional arguments to 'upver' subcommand.\n")
        return

    run_cmd(f"uv version --bump {semver_part}", kind="uv")
