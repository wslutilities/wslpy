import os.path

def isWSL():
    """
    Check whether the system is WSL.

    Returns
    -------
    A boolean value, `True` if it is WSL.
    """
    return os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')

print(isWSL())