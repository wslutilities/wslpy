"""
This is the execution class to execute commands
from different windows executables
"""
from os import path
from .__core__.check import get_sys_drive_prefix, is_interop_enabled, is_wsl
from .__core__.access import __exec_command__


def __pre_check__():
    assert is_wsl(), "This is not a wsl distribution"
    assert is_interop_enabled(), (
        "WSL Interoperability is disabled and WSL Utilities won't work. "
        "Please enable it by:\n"
        "1. open /etc/wsl.conf using root or equivalent editing permission;\n"
        "2. under [interop] section, set enabled to true;\n"
        "3. restart your distribution.\n\nOr, \n"
        "# echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop")


def cmd(command, working_dir=None):
    """
    Execute cmd command.

    Parameters
    ----------
    command : str
        string of `cmd.exe` commands.
    working_dir : str
        working directory of the command. default is None.

    Returns
    -------
    return a CompletedProcess object.
    """
    __pre_check__()
    sysdrv_prefix = get_sys_drive_prefix()
    pt = path.join(sysdrv_prefix, "Windows", "System32", "cmd.exe")
    cmd = [pt, "/c", command]
    p = __exec_command__(cmd, working_dir=working_dir)
    return p


def winps(command, working_dir=None):
    """
    Execute Windows PowerShell(5.*) command.

    Parameter
    ---------
    command : str
        string of `powershell.exe` command.
    working_dir : str
        working directory of the command. default is None.

    Returns
    -------
    return a CompletedProcess object.
    """
    __pre_check__()
    sysdrv_prefix = get_sys_drive_prefix()
    pt = path.join(sysdrv_prefix, "Windows", "System32",
                   "WindowsPowerShell", "v1.0", "powershell.exe")
    cmd = [pt, "-NoProfile", "-NonInteractive", "-Command",
           command]
    p = __exec_command__(cmd, working_dir=working_dir)
    return p
