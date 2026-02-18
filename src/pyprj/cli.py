from clig import Command

from pyprj import nbex, nbmd
from pyprj.newproj import init as initproj


def pyprj():
    """CLI to manage python projects"""
    print(locals())


def docs():
    """Manage documentation"""
    print(locals())


def init():
    """Initialize documentation"""
    pass


def modm():
    """Process modules"""
    pass


def optmetavarmodifier(name: str):
    return f"<{name}>"


kwargs = {"make_shorts": True, "optmetavarmodifier": optmetavarmodifier}
# kwargs.pop("optmetavarmodifier")


def main():
    # fmt: off
    cmd: Command = (
        Command(pyprj, make_shorts=True)
            .add_subcommand(initproj)
            .add_subcommand(docs)
            .new_subcommand(docs)
                .add_subcommand(init, **kwargs) 
                .add_subcommand(nbmd, make_shorts=True)
                .add_subcommand(nbex, **kwargs)
                .end_subcommand(modm, **kwargs)
    )
    # fmt: on
    cmd.run()
