import shutil
import textwrap
from functools import partial

from clig import Command, Context

from pyprj import nbex, nbmd
from pyprj.newproj import init as initproj


def pyprj(ctx: Context):
    """CLI to manage python projects"""
    subcommand = list(vars(ctx.namespace).values())[0]
    if not subcommand:
        ctx.command.run(["--help"])


def docs():
    """Manage documentation"""
    print(locals())


def init():
    """Initialize documentation"""
    pass


def modm():
    """Process modules"""
    pass


def optmetavarmodifier(name: str):
    return f"<{name}>"


def format_help(
    text: str,
    width: int | None = None,
    space: int = 24,
    dedent: bool = True,
    final_newlines: bool = False,
    append_text: str = "",
) -> str:
    text = f"{text}{append_text}"
    width = width or shutil.get_terminal_size().columns
    lines = []
    for line in text.splitlines():
        line = textwrap.dedent(line) if dedent else line
        lines.append(textwrap.fill(text=line, width=width - space, replace_whitespace=False))

    return "\n".join(lines) + ("\n\n" if final_newlines else "")


opthelpmodifier = partial(format_help, width=80, append_text="\nDefaults to '%(default)s'.")


kwargs = {
    "make_shorts": True,
    "optmetavarmodifier": optmetavarmodifier,
    "opthelpmodifier": opthelpmodifier,
    "help_msg": format_help("Show this help message and exit.", width=80),
}


def main():
    # fmt: off
    cmd: Command = (
        Command(pyprj, **kwargs)
            .add_subcommand(initproj, **kwargs)
            .new_subcommand(docs)
                .add_subcommand(init, **kwargs) 
                .add_subcommand(nbmd, make_shorts=True)
                .add_subcommand(nbex, **kwargs)
                .end_subcommand(modm, **kwargs)
    )
    # fmt: on
    cmd.run()
