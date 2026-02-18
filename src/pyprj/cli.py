# %%          Imports
############# Imports ##########################################################################################################

import shutil
import textwrap
from functools import partial

from clig import Command, Context

from pyprj import nbex as gen_jup_notebook_example
from pyprj import nbmd as jup_notebook_to_markdown
from pyprj.docman import doc as manage_documentation
from pyprj.docman import ini as initialize_documentation
from pyprj.docman import modm as modify_normal_py_modules
from pyprj.newproj import ini as initialize_project

# %%          Commands
############# Commands #########################################################################################################


def pyprj(ctx: Context):
    """CLI to manage python projects"""
    subcommand = list(vars(ctx.namespace).values())[0]
    if not subcommand:
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


opthelpmodifier = partial(format_help, width=80, append_text="\nDefaults to '%(default)s'.")


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


def main():
    # fmt: off
    cmd: Command = (
        Command(pyprj, **kwargs_only_help_flag_with_subcmds)
            .add_subcommand(initialize_project, **kwargs)
            .new_subcommand(manage_documentation, **kwargs_only_help_flag_with_subcmds)
                .add_subcommand(initialize_documentation, **kwargs) 
                .add_subcommand(jup_notebook_to_markdown, **kwargs_without_optmetavarmodifier)
                .add_subcommand(gen_jup_notebook_example, **kwargs)
                .end_subcommand(modify_normal_py_modules, **kwargs)
    )
    # fmt: on
    cmd.run()
