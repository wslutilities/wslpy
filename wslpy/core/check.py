from os import path
import subprocess


def is_wsl():
    """
    Check whether the system is WSL.

    Returns
    -------
    A boolean value, `True` if it is WSL.
    """
    return path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')


def is_interop_enabled():
    """
    Checks if interoperablility is enabled.

    Returns
    -------
    A boolean value, `True` if interoperablility is enabled.
    """
    cat_wslInterop = subprocess.getoutput(
        "cat /proc/sys/fs/binfmt_misc/WSLInterop | grep '.*abled'")
    return cat_wslInterop == 'enabled'


def __read_attribute__(file, attr):
    """
    INTERNAL FUNCTION
    Tries to find value after the given attribute.

    Returns
    -------
    Value of the given attr if found
    Else raises Exception('No such attribute found').
    """
    with open(file, mode='r') as f:
        lines = f.readlines()
    for line in lines:
        if line.find(attr) != -1:
            line = line.strip()  # Strip whitespaces
            line = line.replace(attr, "")
            line = line.strip('\"')  # strip ".."
            return line
            break
    raise Exception('No such attribute found')


def detect_distro():
    """
    Reads the /etc/os-release file nad tries to infer
    the the OS form available attributes.

    Returns
    -------
    Name of distribution.
    """
    file = '/etc/os-release'
    distro = __read_attribute__(file, 'NAME=')
    if distro == 'Arch':
        return 'archlinux'
    elif distro == 'Scientific':
        return 'scilinux'
    elif distro == 'Fedora Remix for WSL':
        return 'fedoraremix'
    elif distro == 'Generic':
        os_id = __read_attribute__(file, 'ID_LIKE=')
        if os_id == 'fedora':
            return 'oldfedora'
        else:
            return 'unknown'

    return distro.lower()
