from clig import Context

from .taskscmd import run_task


def docs(ctx: Context):
    """Manage documentation of the project.

    If called without subcommands, runs the task `docs` inside the project.
    Tasks use the tool `taskipy`. Currently are run with the tool `uv`.
    The task `docs` makes docs with `sphinx` in folder `./doc/sphinx`.
    """
    if vars(ctx.namespace)[ctx.command.sub_commands["docs"].subparsers_dest] is None:
        run_task("docs")
