"""wslpy.exec

This is the execution class to execute commands from different windows executables
"""
import subprocess
import os
from wslpy.__init__ import isWSL
import sys


def __isInteropEnabled__():
    cat_wslInterop = subprocess.getoutput(
        "cat /proc/sys/fs/binfmt_misc/WSLInterop | grep '.*abled'")
    return cat_wslInterop == 'enabled'


def isInteropEnabled():
    """
    Checks if interoperablility is enabled.

    Returns
    _______
    A boolean value, `True` if interoperablility is enabled.
    """
    return __isInteropEnabled__()


def preCheck():

    if isWSL():
        if not isInteropEnabled():
            sys.exit(
                "Please enable interop /n Use 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'")
    else:
        sys.exit("This is not a wsl distribution")

def preCheckAssert():

    assert isWSL(),"This is not a wsl distribution"
    assert isInteropEnabled(),"Please enable interop /n Use 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'"


def cmd(command):
    """
    Execute cmd command.

    Parameters
    ----------
    command : str
        string of `cmd.exe` commands.
    """
    #preCheck()
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
    preCheck()
    cmd = u"powershell.exe -NoProfile -NonInteractive -Command \""+command+u"\""
    subprocess.call(cmd, shell=True)


def pwShCr(command):
    """
    Execute PowerShell Core command.

    Parameter
    ---------
    command : str
        string of `pwsh.exe` command.
    """
    preCheck()
    cmd = u"pwsh.exe -NoProfile -NonInteractive -Command \""+command+u"\""
    subprocess.call(cmd, shell=True)
