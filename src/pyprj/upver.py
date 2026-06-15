import shutil
import sys
from pathlib import Path
from typing import Literal

from clig import Arg, data

from .run_cmd import run_cmd
from .taskscmd import build as buill_project


def upver(semver: Arg[Literal["major", "minor", "patch"], data(nargs="?")], build: bool = False, move: bool = False):
    """Update or show project version.

    Currently, it uses the command `uv version`.
    If called without positional arguments, only show the project version.
    .

    Parameters
    ----------
    - `semver` (`Literal["major", "minor", "patch"]`, optional):.
        Semantic version pattern of the updated version.

    - `build` (`bool`, optional): Defaults to `False`.
        Whether to build the project after update version.

    - `move` (`bool`, optional): Defaults to `False`.
        Whether to move files from `dist/` folder to `builds/` folder (before building).
    """

    if not semver:
        error_code: int = run_cmd(f"uv version", kind="uv")
        if error_code != 0:
            sys.exit("\nNo `pyproject.toml` file found in this directory or parent directories.\nIt is not a project yet.\n")
        print(f"\nThe current package is in the version above.")
        print("To update the project version, use a positional argument in the `upver` subcommand:")
        print("> " + " | ".join(["major", "minor", "patch"]))
        print()
        return error_code

    error_code = run_cmd(f"uv version --bump {semver}", kind="uv")
    if error_code != 0:
        sys.exit("\nNo `pyproject.toml` file found in this directory or parent directories.\nIt is not a project yet.\n")

    from .pyproject import __get_pyproject_data, pkg_name, pyproject

    if move:
        dist_dir: Path = pyproject.dirpath / "dist"
        if dist_dir.exists() and dist_dir.is_dir():
            builds_dir: Path = pyproject.dirpath / "builds"
            builds_dir.mkdir(parents=True, exist_ok=True)
            for file_path in dist_dir.glob("*.*"):
                shutil.move(str(file_path), str(builds_dir / file_path.name))
                print("-------------------------")
                print(f"Move file: - {file_path}")
                print(f"To folder: - {builds_dir}")

    if build:
        buill_project()

    about_path: Path = Path(pyproject.dirpath / f"src/{pkg_name}/__about__.py")
    if about_path.exists():
        print("> Updating version in `__about__.py` file")
        pkg_version = __get_pyproject_data()["project"]["version"]
        with open(about_path, "r", encoding="utf-8") as file:
            text: list[str] = file.readlines()
        text: list[str] = [f'__version__ = "{pkg_version}"' if s.startswith("__version__") else s for s in text]
        with open(about_path, "w", encoding="utf-8") as file:
            file.write("".join(text))
        print("done.")
