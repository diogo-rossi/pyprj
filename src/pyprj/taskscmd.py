import sys

from .run_cmd import run_cmd


def run_task(task: str):
    """Run task with taskipy

    Parameters
    ----------
    - `task` (`str`):
        The name of the task to run

    """
    exit_code = run_cmd(f"uv run task {task}", kind="uv")
    if exit_code != 0:
        sys.exit(exit_code)


def test():
    """Run task 'test' inside the project.

    This command only runs the task 'test' inside the project.
    Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
    The task 'test' runs tests with 'pytest' in folder './tests'.
    """
    run_task("test")


def build():
    """Run task 'build' inside the project.

    This command only runs the task 'build' inside the project.
    Tasks use the tool 'taskipy'. Currently are run with the tool 'uv'.
    The task 'build' builds the package with 'uv' in root folder.
    """
    run_task("build")
