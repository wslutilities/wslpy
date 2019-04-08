from pathlib import Path


def __isWSL__():
    try:
        Path('/proc/sys/fs/binfmt_misc/WSLInterop').resolve()
    except FileNotFoundError:
        return False
    else:
        return True

def isWSL():
    """
    Check whether the system is WSL.

    Returns
    -------
    A boolean value, `True` if it is WSL.
    """
    return __isWSL__()
