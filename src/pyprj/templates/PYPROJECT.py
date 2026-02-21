PYPROJECT_EXTRALINES: str = r"""
[project.urls]
Documentation = "{{documentation_page}}"
Issues = "{{source_repo}}/issues"
Source = "{{source_repo}}/blob/main/README.md"

[tool.pytest]
addopts = [
    "-rx",        # Show extra test summary: (x)failed
    "-vv",        # Increase verbosity
    "-s",         # Shortcut for --capture=no (Per-test capturing method)
    "--tb=short", # Traceback print mode = short
]

[tool.black]
line-length = {{line_length}}

[tool.taskipy.tasks]
docs = { cmd = "make html", cwd = "./doc/sphinx", help = "Make docs with sphinx in folder './doc/sphinx'" }
open = { cmd = "index.html", cwd = "./doc/sphinx/build/html", help = "Open sphinx docs in folder './doc/sphinx/build/html'" }
test = { cmd = "pytest", cwd = "./tests", help = "Test with pytest in folder './tests'" }
build = { cmd = "uv build", cwd = ".", help = "Build package" }
publish = { cmd = "pyprj publish", cwd = ".", help = "Publish package to PyPI" }
"""
