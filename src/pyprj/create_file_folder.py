from pathlib import Path


def __create_file(path: str, content: str, newline: str | None = "\n"):
    msg: str = f"> creating file '{path}'"
    print(f"{msg}")
    with open(path, "w", encoding="utf-8", newline=newline) as file:
        file.write(content)


def __create_folder(path: str | Path):
    msg: str = f"> creating folder '{Path(path).as_posix()}/' "
    sep: str = "-" * len(msg)
    print(f"{msg}")
    try:
        Path(path).mkdir(exist_ok=True)
    except:
        print(f"{sep}")
        raise
