import shutil
import textwrap
from functools import partial


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
    glue_lines = [""]
    for line in text.splitlines():
        if not glue_lines[-1].endswith("."):
            glue_lines[-1] = glue_lines[-1] + " " + line
        else:
            glue_lines.append(line)
    for line in glue_lines:
        line = textwrap.dedent(line) if dedent else line
        lines.append(textwrap.fill(text=line, width=width - space, replace_whitespace=False))

    return "\n".join(lines) + ("\n\n" if final_newlines else "")


opthelpmodifier = partial(format_help, width=90, append_text="\nDefaults to '%(default)s'.")


def optmetavarmodifier(name: str):
    return f"<{name.replace("_","-")}>"
