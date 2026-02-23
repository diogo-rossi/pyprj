from pathlib import Path

from .cellfuncs import _generate_example
from .nbex import nbex


def load_ipython_extension(ipython):
    try:
        from IPython.core.magic import Magics, cell_magic, magics_class
    except ImportError as e:
        raise RuntimeError("IPython support is not installed. " "Install with: pip install yourlib[ipython]") from e

    @magics_class
    class MyMagics(Magics):

        @cell_magic
        def writeexample(self, line: str, cell: str):
            nbex(Path.cwd(), only_rename_examples=True)
            lines: list[str] = cell.splitlines(keepends=True)
            example_filename: str = lines[0].strip("# ").strip()
            file_dest_dir = Path.cwd() / (line if line else "examples")
            file_dest_dir.mkdir(exist_ok=True)
            _generate_example(lines, example_filename, file_dest_dir)

    ipython.register_magics(MyMagics)
