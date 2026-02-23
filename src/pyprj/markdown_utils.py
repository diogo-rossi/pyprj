from pathlib import Path


def get_markdown_sections(filepath: Path) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as file:
        lines: list[str] = file.readlines()

    sections: list[str] = [""]
    for line in lines:
        if line.startswith("#"):
            sections.append(line)
        else:
            sections[-1] += line
    return sections


def convert_admonitions_to_myst(text: str) -> str:
    return text
