from enum import Enum


class Color(Enum):
    BLACK = "30"
    BLUE = "34"
    CYAN = "36"
    GREEN = "32"
    MAGENTA = "35"
    RED = "31"
    WHITE = "37"
    YELLOW = "33"
    BOLD = "1"
    ITALIC = "3"


def str_hilight(string: str, *attrs: Color) -> str:
    """Prints string colored

    Parameters
        - ``string`` (``str``): Specifies the string to print
        - ``*attrs`` (``Attr``): Specifies Enum constants of class `Attr` with attributes to use.
            Possible values are::

                BLACK, BLUE, CYAN, GREEN, MAGENTA, RED, WHITE, YELLOW, BOLD, ITALIC
    """
    codes = ";".join([attr.value for attr in attrs])
    return f"\x1b[{codes}m{string}\x1b[0m"


def printcolor(string: str, *attrs: Color):
    print(str_hilight(string, *attrs))
