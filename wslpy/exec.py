"""wslpy.exec

This is the execution class to execute commands
from different windows executables
"""
from .core.check import is_interop_enabled, is_wsl
from .core.access import __exec_command__


def preCheckAssert():
    assert is_wsl(), "This is not a wsl distribution"
    assert is_interop_enabled(), ("Please enable interop /n Use 'echo 1 > "
                                  "/proc/sys/fs/binfmt_misc/WSLInterop'")


def cmd(command, working_dir=None):
    """
    Execute cmd command.

    Parameters
    ----------
    command : str
        string of `cmd.exe` commands.
    """
    preCheckAssert()
    cmd = ["cmd.exe", "/c", command]
    p = __exec_command__(cmd, working_dir=working_dir)
    return p


def winps(command, working_dir=None):
    """
    Execute Windows PowerShell(5.*) command.

    Parameter
    ---------
    command : str
        string of `powershell.exe` command.
    """
    preCheckAssert()
    cmd = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
           command]
    p = __exec_command__(cmd, working_dir=working_dir)
    return p
