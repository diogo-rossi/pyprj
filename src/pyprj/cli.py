# %%          Imports
############# Imports ##########################################################################################################


from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version

from clig import Arg, Command, Context, data

from .docs import docs
from .help_modifiers import format_help, opthelpmodifier, optmetavarmodifier
from .init_docs import init
from .init_proj import init as inip
from .modm import modm
from .nbex import nbex
from .nbmd import nbmd
from .publish import publish
from .taskscmd import build, test
from .upver import upver

try:
    __version__ = pkg_version("pyprj")
except PackageNotFoundError:
    __version__ = "0.0.0"


# %%          Commands
############# Commands #########################################################################################################


def pyprj(ctx: Context):
    """A CLI to manage python projects with predefined tools."""
    if vars(ctx.namespace)[ctx.command.subparsers_dest] is None:
        ctx.command.run(["--help"])


# %%          CLI customization
############# CLI customization ################################################################################################


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


def main() -> None:
    # fmt: off
    cmd: Command = (
        Command(pyprj, version=True, epilog=" ", **kwargs_only_help_flag_with_subcmds)
            .add_subcommand(inip, **kwargs)
            .add_subcommand(test, **kwargs)
            .new_subcommand(docs, **kwargs_only_help_flag_with_subcmds)
                .add_subcommand(init, **kwargs) 
                .add_subcommand(nbex, **kwargs)
                .add_subcommand(nbmd, **kwargs_without_optmetavarmodifier)
                .end_subcommand(modm, **kwargs)
            .add_subcommand(upver, epilogmodifier=lambda s: f"{s}\n ", **kwargs)
            .add_subcommand(build, **kwargs)
            .add_subcommand(publish, **kwargs)
    )
    # fmt: on
    return cmd.run()
