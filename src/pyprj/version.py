from typing import Literal

from clig import Arg, data

from .run_cmd import run_cmd


def version(semver_part: Arg[Literal["major", "minor", "patch"], data(nargs="?")]):
    """Update or show project version

    If called without positional arguments, only show the project version.
    """
    if not semver_part:
        from .pyproject import pkg_name, pkg_version

        print(f"Package '{pkg_name}' version: {pkg_version}")
        return

    run_cmd(f"uv version --bump {semver_part}", kind="uv")
