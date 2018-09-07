from pathlib import Path

def __isWSL__():
    try:
        Path('/proc/sys/fs/binfmt_misc/WSLInterop').resolve()
    except FileNotFoundError:
        return False
    else:
        return True

#: A boolean value to check whether the system is WSL.
isWSL=__isWSL__()
