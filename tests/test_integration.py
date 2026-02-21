from resources import notebook_filepath

import pyprj.ndmd as genbdoc


def test_write_md_file():
    genbdoc.nbmd(notebook_filepath)
