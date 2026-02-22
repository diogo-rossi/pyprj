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
    │    └─── {pkg_name}
    │            __init__.py{cli_file}
    │            py.typed
    ├─── tests
    │
    .gitignore
    .prettierrc.json
    .python-version
    .readthedocs.yaml
    pyproject.toml
    README.md
    LICENSE.txt
```
"""
