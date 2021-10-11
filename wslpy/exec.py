"""wslpy.exec

This is the execution class to execute commands
from different windows executables
"""
import subprocess

from wslpy.core.check import is_interop_enabled, is_wsl


def preCheckAssert():
    assert is_wsl(), "This is not a wsl distribution"
    assert is_interop_enabled(), ("Please enable interop /n Use 'echo 1 > "
                                  "/proc/sys/fs/binfmt_misc/WSLInterop'")


def cmd(command):
    """
    Execute cmd command.

    Parameters
    ----------
    command : str
        string of `cmd.exe` commands.
    """
    preCheckAssert()
    cmd = u"cmd.exe /c \""+command+u"\""
    subprocess.call(cmd, shell=True)


def pwSh(command):
    """
    Execute PowerShell(5.*) command.

    Parameter
    ---------
    command : str
        string of `powershell.exe` command.
    """
    preCheckAssert()
    cmd = (u"powershell.exe -NoProfile "
           u"-NonInteractive -Command \"{}\"").format(command)
    subprocess.call(cmd, shell=True)


def pwShCr(command):
    """
    Execute PowerShell Core command.

    Parameter
    ---------
    command : str
        string of `pwsh.exe` command.
    """
    preCheckAssert()
    cmd = u"pwsh.exe -NoProfile -NonInteractive -Command \""+command+u"\""
    subprocess.call(cmd, shell=True)
