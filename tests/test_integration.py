from resources import notebook_filepath

import pyprj.nbmd as genbdoc


def test_write_md_file():
    genbdoc.nbmd(notebook_filepath)
