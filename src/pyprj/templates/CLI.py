CLI_PY: str = r'''import clig


def clicmd():
    """Say hello"""
    print("\nHello from '{{pkg_name}}' cli!\n")


def main():
    clig.run(clicmd)


if __name__ == "__main__":
    main()
'''
