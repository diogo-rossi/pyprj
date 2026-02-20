from .run_cmd import run_cmd


def publish():
    """Publish package to PyPI

    Uses token from file '.vscode/pyprj.json'
    """
    from .pyprj_json_data import json_content, published_versions, save_content, token
    from .pyproject import pyproject, version

    if version in published_versions:
        print(f"\nThe version '{version}' has already been published. Please, update it first.\n")
        return

    if not token:
        print("\nPlease, provide a token in the file '.vscode/pyprj.json'\n")
        return

    error_code: int = run_cmd(f"uv publish {(pyproject.dirpath / 'dist/*').as_posix()} --token {token}", kind="uv")
    if error_code == 0:
        published_versions.append(version)
        save_content(json_content)
