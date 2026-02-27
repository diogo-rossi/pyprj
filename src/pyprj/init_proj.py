import os
import sys
from datetime import datetime
from functools import partial

from clig import Arg, data

from .create_file_folder import __create_file, __create_folder
from .help_modifiers import format_help
from .run_cmd import SEP, run_cmd
from .templates.CLI import CLI_PY
from .templates.GITIGNORE import GITIGNORE
from .templates.LAUNCH import LAUNCH_JSON
from .templates.LICENSE import LICENSE_TXT
from .templates.PRETTIER import PRETTIER_JSON
from .templates.PYPRJ import PYPRJ_JSON
from .templates.PYPROJECT import PYPROJECT_CLI_SCRIPT, PYPROJECT_EXTRALINES
from .templates.README import README_MD
from .templates.READTHEDOCS import READTHEDOCS_YAML
from .templates.SETTINGS import SETTINGS_JSON
from .templates.TASKS import TASKS_JSON
from .templates.TREE import TREE

modifier = partial(format_help, width=90)

year = datetime.now().year


def init(
    name: str | None = None,
    python_version: str = "3.12",
    black_line_length: int = 128,
    cli: Arg[str | bool, data(nargs="?", const=True, helpmodifier=modifier, metavar="<cli-name>")] = False,
    no_about: bool = False,
):
    """Create a new project for a python package.

    Parameters
    ----------
    - `name` (`str | None`, optional): Defaults to `None`.
        The name of the project. If `None`, use the current directory's name.

    - `python_version` (`str`, optional): Defaults to `"3.12"`.
        The Python interpreter version to use to determine the minimum supported Python version.

    - `black_line_length` (`int`, optional): Defaults to `128`.
        Line length parameter to use with `black`.

    - `cli` (`str | bool`, optional): Defaults to `False`.
        Optional CLI script name. If omitted, No CLI command is added.
        If provided without a value, the CLI command name defaults to
        the name of the package.

    - `no_about` (`bool`, optional): Defaults to `False`.
        Whether to not add an `__about__.py` file in the project's `src` folder with
        the `__version__` property. The default (`False`) will add the file.
    """

    exit_code = run_cmd("git init", "git")
    if exit_code != 0:
        sys.exit(exit_code)

    for configvar in ["author", "email"]:
        userconfig = "name" if configvar == "author" else configvar
        envvar = f"PYPRJ_{configvar.upper()}"
        if envvar in os.environ:
            variable = os.environ[envvar]
            print(f"Found env variable {envvar} = {variable}")
            exit_code = run_cmd(cmd=f'git config --local user.{userconfig} "{variable}"', kind="git", add_sep=False)
            if exit_code != 0:
                sys.exit(exit_code)
        else:
            print(f"No env variables found, using the following git {configvar}:")
            os.system(f"git config get user.{userconfig}")
            print()

    project_name_arg = f"--name {name} " if name is not None else ""
    print(f"Initializing project {project_name_arg}")
    cmd = f"uv init --lib --author-from git --python {python_version} {project_name_arg}"
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    print(f"{SEP}\nAdding dev packages:")
    dev_pkgs: list[str] = ["black", "taskipy"]
    cmd: str = f"uv add --dev {' '.join(dev_pkgs)}"
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    print(f"{SEP}\nAdding test packages:")
    test_pkgs: list[str] = ["pytest"]
    cmd: str = f"uv add --group test {' '.join(test_pkgs)}"
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    if cli:
        print(f"{SEP}\nAdding CLI packages:")
        dep_pkgs: list[str] = ["clig"]
        cmd: str = f"uv add {' '.join(dep_pkgs)}"
        exit_code = run_cmd(cmd, kind="uv", add_sep=False)
        if exit_code != 0:
            sys.exit(exit_code)

    cmd: str = "uv sync --all-groups"
    print(f"{SEP}\nSyncing packages")
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    from .pyproject import author_email, author_name, documentation_page, pkg_name, source_repo

    msg: str = f"> editing file 'pyproject.toml'"
    cli = pkg_name if cli and cli == True else cli
    pyproject_cli_script = PYPROJECT_CLI_SCRIPT.replace("{{cli_name}}", cli).replace("{{pkg_name}}", pkg_name) if cli else ""
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}")
    with open("pyproject.toml", "r", encoding="utf-8") as file:
        content: str = file.read()
    content = content.replace('readme = "README.md"', 'readme = "README.md"\nlicense = "MIT"')
    with open("pyproject.toml", "w", encoding="utf-8", newline="\n") as file:
        file.write(
            content
            + pyproject_cli_script
            + PYPROJECT_EXTRALINES.replace("{{line_length}}", str(black_line_length))
            .replace("{{source_repo}}", source_repo)
            .replace("{{documentation_page}}", documentation_page)
        )

    __create_folder("tests")
    __create_folder(".vscode")
    __create_file(".vscode/settings.json", SETTINGS_JSON.replace("{{line_length}}", str(black_line_length)))
    __create_file(".vscode/tasks.json", TASKS_JSON)
    __create_file(".vscode/launch.json", LAUNCH_JSON)
    __create_file(".vscode/pyprj.json", PYPRJ_JSON)
    __create_file(".prettierrc.json", PRETTIER_JSON)
    __create_file(".readthedocs.yaml", READTHEDOCS_YAML.replace("{{python_version}}", python_version))
    __create_file(".gitignore", GITIGNORE)
    __create_file("README.md", README_MD.replace("{{pkg_name}}", pkg_name), newline=None)
    __create_file(
        "LICENSE.txt",
        LICENSE_TXT.replace("{{author_name}}", author_name)
        .replace("{{author_email}}", author_email)
        .replace("{{year}}", str(year)),
    )

    if cli:
        __create_file(f"src/{pkg_name}/cli.py", CLI_PY.replace("{{pkg_name}}", pkg_name), newline=None)

    if not no_about:
        __create_file(f"src/{pkg_name}/__about__.py", "", newline=None)

    sep: str = "-" * len(msg)
    print(sep)

    print("\nCreated a project for a python package with the following structure:")
    print(
        TREE.format(
            pkg_name=pkg_name,
            about_file="\n    │            __about__.py" if not no_about else "",
            cli_file="\n    │            cli.py" if cli else "",
        )
    )
    if cli:
        print("With the following packages in dependencies:")
        print("- " + " | ".join(dep_pkgs))
        print()
    print("With the following packages in the `dev` dependency group:")
    print("- " + " | ".join(dev_pkgs))
    print()
    print("With the following packages in the `test` dependency group:")
    print("- " + " | ".join(test_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")
