from pathlib import Path

from clig import Arg, Context, data


def modm(filepath: Arg[list[Path] | Path | None, data(nargs="*", make_flag=False)] = None):
    """Process documentation in modules.

    Parameters
    ----------
    - `filepath` (`Arg[list[Path]  |  Path  |  None`, optional): Defaults to `None`.
        The filepath or filepaths of modules (.py) to process.
        If `None` (default), process all python files from the current directory.
    """
    print("\nTODO: not yet implemented!\n")
