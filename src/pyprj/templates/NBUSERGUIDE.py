NBUSERGUIDE: str = r"""{
    "cells": [
        {
            "cell_type": "markdown",
            "id": "addd5238",
            "metadata": {},
            "source": [
                "# Userguide\n",
                "\n",
                "Userguide text"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "c2a8310a",
            "metadata": {},
            "source": [
                "## Code cell:\n",
                "\n",
                "This is a cell code running in the virtual environment."
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
                "This is a file code running in the virtual environment."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "id": "9c01f9c0",
            "metadata": {},
            "outputs": [],
            "source": [
                "%%python -c \"import os; print('CWD:', str(os.getcwd())[str(os.getcwd()).index('doc'):]); os.system('pyprj docs nbex')\"\n",
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
                "This is a shell cell running the previous example."
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
