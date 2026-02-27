NBUSERGUIDE: str = r"""{
    "cells": [
        {
            "cell_type": "code",
            "execution_count": null,
            "id": "c290273e",
            "metadata": {
                "tags": [
                    "to_hide"
                ]
            },
            "outputs": [],
            "source": [
                "%load_ext pyprj"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "addd5238",
            "metadata": {},
            "source": [
                "# Userguide\n",
                "\n",
                "Introduction text to the userguid document"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "c2a8310a",
            "metadata": {},
            "source": [
                "## Code cell:\n",
                "\n",
                "This is a cell code running in the virtual environment. It is rendered with the `>>>` layout. "
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "id": "e571d4a2",
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "print(\"This is a cell code running in the virtual environment.\")\n",
                "print(\"Interpreter:\", sys.executable[sys.executable.index(\".venv\"):])"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "21ff05ad",
            "metadata": {},
            "source": [
                "## File cell\n",
                "\n",
                "This is a file code running in the virtual environment. It is rendered as is (without the `%%` command)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "id": "9c01f9c0",
            "metadata": {},
            "outputs": [],
            "source": [
                "%%writeexample\n",
                "# example01.py\n",
                "import sys\n",
                "import os\n",
                "\n",
                "print(\"This is the file 'examples/example01.py' running in a virtual environment.\")\n",
                "print(\"Interpreter:\", sys.executable[sys.executable.index(\".venv\") :])\n",
                "print(\"Current working directory: \", os.getcwd())"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "b8a31c9e",
            "metadata": {},
            "source": [
                "## Shell cell\n",
                "\n",
                "This is a shell cell running the previous example. It is rendered with `>` as shell prompt."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "id": "e705586e",
            "metadata": {},
            "outputs": [],
            "source": [
                "! python examples/example01.py"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}
"""
