from os import path, listdir

from .access import distro_info


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
    Checks if interoperability is enabled.

    Returns
    -------
    A boolean value, `True` if interoperability is enabled.
    """
    if is_wsl():
        if path.exists("/etc/wsl.conf"):
            from configparser import ConfigParser
            c = ConfigParser()
            c.read("/etc/wsl.conf")
            if c.has_option('interop', 'enabled'):
                value = c['interop']['enabled']
                return value.lower() == 'true'
        with open('/proc/sys/fs/binfmt_misc/WSLInterop', 'r') as f:
            interop_str = f.read()
            value = interop_str.split('\n')[0]
    return value == 'enabled'


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
    the OS form available attributes.

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


def get_mount_prefix():
    """
    This function returns the prefix for the current windows mount location,
    aka the Interop Prefix.

    Returns
    -------
    The interop prefix. default is ``/mnt/``.
    """
    from configparser import ConfigParser

    win_location = '/mnt/'
    if path.exists('/etc/wsl.conf'):
        config = ConfigParser()
        config.read('/etc/wsl.conf')
        if config.has_option('automount', 'root'):
            win_location = config.get('automount', 'root')

    return win_location


def get_sys_drive_prefix():
    """
    This function returns the prefix for the current windows mount locaution,
    aka the Sys Drive Prefix.

    Returns
    -------
    The sys drive prefix. default is ``/mnt/c``.
    """
    ip = get_mount_prefix()
    sys_drive = 'c'
    drive_list = listdir(ip)
    drive_list = [a for a in drive_list if len(a) == 1]
    for drive in drive_list:
        sys32_path = path.join(ip, drive, 'Windows', 'System32')
        if path.exists(sys32_path):
            sys_drive = drive
            break
    return path.join(ip, sys_drive)


def wsl_version():
    """
    This function returns the version of WSL.

    Returns
    -------
    The version of WSL.
    """
    if is_interop_enabled():
        info = distro_info()
        flag = int(info['Flags']['value'], 0)
        if flag // 8 == 1:
            return 2
        else:
            return 1
    else:
        import re
        from platform import release
        rel = release()
        if re.match(r'^4\.\d\.\d-\d{5}-Microsoft', rel) is not None:
            return 1
        else:
            return 2
