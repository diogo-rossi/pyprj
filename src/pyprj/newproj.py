import os
import sys

TREE: str = """
```
    {pkg_name}
    ├─── .venv # -> virtual environment
    ├─── .vscode
    │        settings.json
    │        tasks.json
    │
    ├─── src
    │    └─── mypkg
    │            __init__.py
    │            py.typed
    .gitignore
    .python-version
    pyproject.toml
    README.md
```
"""

GITIGNORE: str = """# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
"""

PYPROJECT_EXTRALINES: str = r"""
[tool.pytest]
addopts = [
    "-rx",        # Show extra test summary: (x)failed
    "-vv",        # Increase verbosity
    "-s",         # Shortcut for --capture=no (Per-test capturing method)
    "--tb=short", # Traceback print mode = short
]

[tool.black]
line-length = {{line_length}}

[tool.taskipy.tasks]
docs = { cmd = "make html", cwd = "./doc/sphinx", help = "Make docs with sphinx in folder './doc/sphinx'" }
open = { cmd = "index.html", cwd = "./doc/sphinx/build/html", help = "Open sphinx docs in folder './doc/sphinx/build/html'" }
test = { cmd = "pytest", cwd = "./tests", help = "Test with pytest in folder './tests'" }
"""

SETTINGS_JSON: str = r"""{
    "[python]": {
        "editor.rulers": [
            {
                "column": {{line_length}},
                "color": "#36a3f0"
            }
        ],
        "rewrap.wrappingColumn": 0
    },
    "black-formatter.args": [
        "--line-length",
        "{{line_length}}"
    ],
    "isort.args": [
        "--line-length",
        "{{line_length}}"
    ],
    "python.testing.pytestArgs": [
        "tests",
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.formatOnType": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "always"
    },
}"""

TASKS_JSON = r"""{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Make sphinx docs with taskipy in folder './docs/sphinx'",
            "type": "shell",
            "command": "uv run task docs",
        },
        {
            "label": "Run pytest with taskipy in folder './tests'",
            "type": "shell",
            "command": "uv run task test",
        },
        {
            "label": "Open docs with taskipy in folder './docs/sphinx/build/html'",
            "type": "shell",
            "command": "uv run task open",
        }
    ]
}"""


def init(
    python: str = "3.12",
    black_line_length: int = 128,
):
    """Create a new project for a python package.

    Parameters
    ----------
    - `python` (`str`, optional): Defaults to `"3.12"`.
        The Python interpreter to use to determine the minimum supported Python version.

    - `black_line_length` (`int`, optional): Defaults to `128`.
        Line length parameter to use with `black`.
    """

    cmd: str = f"git init"
    msg: str = f"> running git comand: `{cmd}`"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}\n{sep}")
    exit_code = os.system(cmd)
    if exit_code != 0:
        sys.exit(exit_code)

    if "PYPRJ_AUTHOR" in os.environ:
        author = os.environ["PYPRJ_AUTHOR"]
        cmd: str = f'git config --local user.name "{author}"'
        msg: str = f"> running git comand: `{cmd}`"
        sep: str = "-" * len(msg)
        print(f"{sep}\n{msg}")
        exit_code = os.system(cmd)
        if exit_code != 0:
            sys.exit(exit_code)

    if "PYPRJ_EMAIL" in os.environ:
        email = os.environ["PYPRJ_EMAIL"]
        cmd: str = f'git config --local user.email "{email}"'
        msg: str = f"> running git comand: `{cmd}`"
        sep: str = "-" * len(msg)
        print(f"{msg}")
        exit_code = os.system(cmd)
        if exit_code != 0:
            sys.exit(exit_code)

    cmd: str = f"uv init --author-from git --python {python} --lib"
    msg: str = f"> running uv comand: `{cmd}`"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}\n{sep}")
    exit_code = os.system(cmd)
    if exit_code != 0:
        sys.exit(exit_code)

    from .pyproject import pkg_name

    dev_pkgs: list[str] = ["black", "pytest", "taskipy"]
    cmd: str = f"uv add --dev {' '.join(dev_pkgs)}"
    msg: str = f"> Adding 'dev' packages, running uv comand: `{cmd}`"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}\n{sep}")
    exit_code = os.system(cmd)
    if exit_code != 0:
        sys.exit(exit_code)

    msg: str = f"> creating folder '.vscode' "
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}")
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

    msg: str = f"> creating file '.gitignore'"
    print(f"{msg}")
    with open(".gitignore", "w", encoding="utf-8") as file:
        file.write(GITIGNORE)

    msg: str = f"> editing file 'pyproject.toml'"
    sep: str = "-" * len(msg)
    print(f"{msg}\n{sep}")
    with open("pyproject.toml", "a", encoding="utf-8") as file:
        file.write(PYPROJECT_EXTRALINES.replace("{{line_length}}", str(black_line_length)))

    print("\nCreated a project for a python package with the following structure:")
    print(TREE.format(pkg_name=pkg_name))
    print("With the follwing packages in the `dev` dependency group:")
    print("- " + " ".join(dev_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")
