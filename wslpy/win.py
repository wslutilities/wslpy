from wslpy.core.check import get_mount_prefix, get_sys_drive_prefix
from wslpy.core.access import distro_info, registry


def get_current_execuable():
    """
    Get current exes of the current WSL (for ones that have).
    """
    import os
    from wslpy.convert import to_wsl
    from wslpy.exec import winps

    _distro_info = distro_info()
    if "PackageFamilyName" in _distro_info:
        pname = _distro_info["PackageFamilyName"]['value']
        p = winps("[Environment]::GetFolderPath('LocalApplicationData')")
        if p.returncode:
            raise Exception("Failed to get LocalApplicationData")
        raw_win_path = p.stdout.replace("\r\n", "")
        win_path = raw_win_path + "\\Microsoft\\WindowsApps\\" + pname
        exe_real_loc = to_wsl(win_path)
        return os.listdir(exe_real_loc)[0]
    else:
        return None


__all__ = [
    "get_current_execuable",
    "get_mount_prefix",
    "get_sys_drive_prefix",
    "registry",
    ]
