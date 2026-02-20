import os
import sys

from .run_cmd import SEP, run_cmd

TREE: str = """
```
    {pkg_name}
    ├─── .venv # -> virtual environment
    ├─── .vscode
    │        settings.json
    │        tasks.json
    │        launch.json
    │        pyprj.json
    │
    ├─── src
    │    └─── mypkg
    │            __init__.py
    │            py.typed
    ├─── tests
    │
    .gitignore
    .prettierrc.json
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

# Example folder in sphinx docs
doc/sphinx/source/notebooks/examples/
"""

PYPROJECT_EXTRALINES: str = r"""
[project.urls]
Documentation = "{{documentation_page}}"
Issues = "{{source_repo}}/issues"
Source = "{{source_repo}}/blob/main/README.md"

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
build = { cmd = "uv build", cwd = ".", help = "Build package" }
publish = { cmd = "pyprj publish", cwd = ".", help = "Publish package to PyPI" }
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
    "[markdown]": {
        "editor.wordWrap": "on",
        "editor.quickSuggestions": {
            "comments": "on",
            "strings": "on",
            "other": "on"
        },
        "files.trimTrailingWhitespace": false,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.rulers": [
            {
                "column": 80,
                "color": "#8a8a8a"
            }
        ],
        "rewrap.wrappingColumn": 0,
        "prettier.proseWrap": "always",
        "prettier.printWidth": 80,
        "prettier.endOfLine": "auto",
    },
}"""

PRETTIER_JSON: str = """{
    "overrides": [
        {
            "files": "*.md",
            "options": {
                "proseWrap": "always",
                "printWidth": 80,
                "endOfLine": "auto"
            }
        }
    ]
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
        },
        {
            "label": "Update version of package with uv",
            "type": "shell",
            "command": "uv version --bump ${input:semver}",
        },
        {
            "label": "Build package with taskipy in root folder",
            "type": "shell",
            "command": "uv run task build",
        },
        {
            "label": "Publish package with uv using taskipy and pyprj",
            "type": "shell",
            "command": "uv run task publish",
        }
    ],
    "inputs": [
        {
            "id": "semver",
            "type": "pickString",
            "options": [
                "major",
                "minor",
                "patch"
            ],
            "description": "Semantic version part",
            "default": "minor"
        }
    ]
}"""

LAUNCH_JSON: str = r"""{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python debug: Current File in its folder",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}"
        },
        {
            "name": "Python debug: Current File in root folder",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        }
    ]
}
"""

PYPRJ_JSON: str = """{
    "token": "",
    "published_versions": []
}"""


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

    project_name_arg = f"--name {name} " if name is not None else ""
    print(f"Initializing project {project_name_arg}")
    cmd = f"uv init --lib --author-from git --python {python} {project_name_arg}"
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    print(f"{SEP}\nAdding dev packages:")
    dev_pkgs: list[str] = ["black", "pytest", "taskipy"]
    cmd: str = f"uv add --dev {' '.join(dev_pkgs)}"
    exit_code = run_cmd(cmd, kind="uv", add_sep=False)
    if exit_code != 0:
        sys.exit(exit_code)

    from .pyproject import documentation_page, pkg_name, source_repo

    msg: str = f"> editing file 'pyproject.toml'"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}")
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
    sep: str = "-" * len(msg)
    print(f"{msg}\n{sep}")
    with open(".gitignore", "w", encoding="utf-8") as file:
        file.write(GITIGNORE)

    print("\nCreated a project for a python package with the following structure:")
    print(TREE.format(pkg_name=pkg_name))
    print("With the follwing packages in the `dev` dependency group:")
    print("- " + " ".join(dev_pkgs))
    print("\nPlease, look at the `pyproject.toml` file for additional info.\n")
