import os
import sys
from datetime import datetime

from .run_cmd import SEP, run_cmd
from .templates.GITIGNORE import GITIGNORE
from .templates.LAUNCH import LAUNCH_JSON
from .templates.LICENSE import LICENSE_TXT
from .templates.PRETTIER import PRETTIER_JSON
from .templates.PYPRJ import PYPRJ_JSON
from .templates.PYPROJECT import PYPROJECT_EXTRALINES
from .templates.README import README_MD
from .templates.SETTINGS import SETTINGS_JSON
from .templates.TASKS import TASKS_JSON
from .templates.TREE import TREE

year = datetime.now().year


def init(
    name: str | None = None,
    python: str = "3.12",
    black_line_length: int = 128,
):
    """Create a new project for a python package.

    Parameters
    ----------
    - `name` (`str | None`, optional): Defaults to `None`.
        The name of the project. If `None`, use the current directory's name.

    - `python` (`str`, optional): Defaults to `"3.12"`.
        The Python interpreter to use to determine the minimum supported Python version.

    - `black_line_length` (`int`, optional): Defaults to `128`.
        Line length parameter to use with `black`.
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
    cmd = f"uv init --lib --author-from git --python {python} {project_name_arg}"
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

    cmd: str = "uv sync --all-groups"
    print(f"{SEP}\nSyncing packages")
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    from .pyproject import author_email, author_name, documentation_page, pkg_name, source_repo

    msg: str = f"> editing file 'pyproject.toml'"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}")

    with open("pyproject.toml", "r", encoding="utf-8") as file:
        content: str = file.read()

    content = content.replace('readme = "README.md"', 'readme = "README.md"\nlicense = "MIT"')

    with open("pyproject.toml", "w", encoding="utf-8", newline="\n") as file:
        file.write(content)

    with open("pyproject.toml", "a", encoding="utf-8") as file:
        file.write(
            PYPROJECT_EXTRALINES.replace("{{line_length}}", str(black_line_length))
            .replace("{{source_repo}}", source_repo)
            .replace("{{documentation_page}}", documentation_page)
        )

    msg: str = f"> creating folder 'tests/' "
    sep: str = "-" * len(msg)
    print(f"{msg}")
    try:
        os.mkdir("tests")
    except:
        print(f"{sep}")
        raise

    msg: str = f"> creating folder '.vscode' "
    print(f"{msg}")
    try:
        os.mkdir(".vscode")
    except:
        print(f"{sep}")
        raise

    msg: str = f"> creating file '.vscode/settings.json'"
    print(f"{msg}")
    with open(".vscode/settings.json", "w", encoding="utf-8") as file:
        file.write(SETTINGS_JSON.replace("{{line_length}}", str(black_line_length)))

    msg: str = f"> creating file '.vscode/tasks.json'"
    print(f"{msg}")
    with open(".vscode/tasks.json", "w", encoding="utf-8") as file:
        file.write(TASKS_JSON)

    msg: str = f"> creating file '.vscode/launch.json'"
    print(f"{msg}")
    with open(".vscode/launch.json", "w", encoding="utf-8") as file:
        file.write(LAUNCH_JSON)

    msg: str = f"> creating file '.vscode/pyprj.json'"
    print(f"{msg}")
    with open(".vscode/pyprj.json", "w", encoding="utf-8") as file:
        file.write(PYPRJ_JSON)

    msg: str = f"> creating file '.prettierrc.json'"
    print(f"{msg}")
    with open(".prettierrc.json", "w", encoding="utf-8") as file:
        file.write(PRETTIER_JSON)

    msg: str = f"> creating file '.gitignore'"
    print(f"{msg}")
    with open(".gitignore", "w", encoding="utf-8") as file:
        file.write(GITIGNORE)

    msg: str = f"> creating file 'README.md'"
    print(f"{msg}")
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(README_MD.replace("{{pkg_name}}", pkg_name))

    msg: str = f"> creating file 'LICENSE.txt'"
    print(f"{msg}")
    with open("LICENSE.txt", "w", encoding="utf-8") as file:
        file.write(
            LICENSE_TXT.replace("{{author_name}}", author_name)
            .replace("{{author_email}}", author_email)
            .replace("{{year}}", str(year))
        )

    sep: str = "-" * len(msg)
    print(sep)

    print("\nCreated a project for a python package with the following structure:")
    print(TREE.format(pkg_name=pkg_name))
    print("With the follwing packages in the `dev` dependency group:")
    print("- " + " | ".join(dev_pkgs))
    print()
    print("With the follwing packages in the `dev` dependency group:")
    print("- " + " | ".join(test_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")
