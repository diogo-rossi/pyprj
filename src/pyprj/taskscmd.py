import os
import sys


def run_task(task: str):
    cmd: str = f"uv run task {task}"
    msg: str = f"> running comand: `{cmd}`"
    sep: str = "-" * len(msg)
    print(f"{sep}\n{msg}\n{sep}")
    exit_code = os.system(cmd)
    if exit_code != 0:
        sys.exit(exit_code)


def test():
    """Run task 'test' inside the project.

    This command only runs the task 'test' inside the project.
    Tasks use the tool 'taskipy'. Currently are run with the tool 'uv.'
    The task 'test' runs tests with 'pytest' in folder './tests'.
    """
    run_task("test")
