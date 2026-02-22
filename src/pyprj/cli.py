# %%          Imports
############# Imports ##########################################################################################################

import shutil
import textwrap
from functools import partial
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from typing import Any

from clig import Arg, Command, Context, data

from .docs import docs
from .init_docs import init
from .init_proj import init as inip
from .modm import modm
from .nbex import nbex
from .ndmd import nbmd
from .publish import publish
from .taskscmd import build, test
from .upver import upver

try:
    __version__ = pkg_version("pyprj")
except PackageNotFoundError:
    __version__ = "0.0.0"


# %%          Commands
############# Commands #########################################################################################################


def pyprj(
    ctx: Context,
    version: Arg[str, data(action="version", version=f"%(prog)s {__version__}")],
):
    """A CLI to manage python projects with predefined tools."""
    if vars(ctx.namespace)[ctx.command.subparsers_dest] is None:
        ctx.command.run(["--help"])


# %%          CLI customization
############# CLI customization ################################################################################################


def format_help(
    text: str,
    width: int | None = None,
    space: int = 24,
    dedent: bool = True,
    final_newlines: bool = True,
    append_text: str = "",
) -> str:
    text = f"{text}{append_text}"
    width = width or shutil.get_terminal_size().columns
    lines = []
    for line in text.splitlines():
        line = textwrap.dedent(line) if dedent else line
        lines.append(textwrap.fill(text=line, width=width - space, replace_whitespace=False))

    return "\n".join(lines) + ("\n\n" if final_newlines else "")


opthelpmodifier = partial(format_help, width=93, append_text=" Defaults to '%(default)s'.")


def optmetavarmodifier(name: str):
    return f"<{name.replace("_","-")}>"


kwargs = {
    "make_shorts": True,
    "optmetavarmodifier": optmetavarmodifier,
    "opthelpmodifier": opthelpmodifier,
    "help_msg": format_help("Show this help message and exit.", width=80),
}

kwargs_only_help_flag_with_subcmds = kwargs.copy()
kwargs_only_help_flag_with_subcmds["help_msg"] = format_help("Show this help message and exit.", width=80, final_newlines=False)
kwargs_only_help_flag_with_subcmds.pop("opthelpmodifier")

kwargs_without_optmetavarmodifier = kwargs.copy()
kwargs_without_optmetavarmodifier.pop("optmetavarmodifier")


# %%          Main function
############# Main function ####################################################################################################


def main() -> int:
    # fmt: off
    cmd: Command = (
        Command(pyprj, **kwargs_only_help_flag_with_subcmds)
            .add_subcommand(inip, **kwargs)
            .add_subcommand(test, **kwargs)
            .new_subcommand(docs, **kwargs_only_help_flag_with_subcmds)
                .add_subcommand(init, **kwargs) 
                .add_subcommand(nbex, **kwargs)
                .add_subcommand(nbmd, **kwargs_without_optmetavarmodifier)
                .end_subcommand(modm, **kwargs)
            .add_subcommand(upver, **kwargs)
            .add_subcommand(build, **kwargs)
            .add_subcommand(publish, **kwargs)
    )
    # fmt: on
    return cmd.run()
