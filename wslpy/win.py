"""
Provides easy access to the Windows information
"""
from .__core__.access import distro_info, registry
from wslpy.exec import winps


def get_current_executable():
    """
    Get current exes of the current WSL (for ones that have)

    Returns
    -------
    A string of the executables
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


def get_display_scaling():
    """
    Get Windows Display Scaling

    Returns
    -------
    A number of the current display scaling
    """
    command = """
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Drawing;

public class DPI {
    [DllImport("gdi32.dll")]
    static extern int GetDeviceCaps(IntPtr hdc, int nIndex);

    public enum DeviceCap {
    VERTRES = 10,
    DESKTOPVERTRES = 117
    }

    public static float scaling() {
    Graphics g = Graphics.FromHwnd(IntPtr.Zero);
    IntPtr desktop = g.GetHdc();
    int LogicalScreenHeight = GetDeviceCaps(desktop, (int)DeviceCap.VERTRES);
    int PhysicalScreenHeight = GetDeviceCaps(desktop,
        (int)DeviceCap.DESKTOPVERTRES);

    return (float)PhysicalScreenHeight / (float)LogicalScreenHeight;
    }
}
'@ -ReferencedAssemblies 'System.Drawing.dll'

[Math]::round([DPI]::scaling(), 2) * 100
"""

    p = winps(command)
    if p.returncode:
        raise Exception("Failed to get display scaling: ", p.stderr)
    dscale = int(p.stdout.rstrip()) / 100
    return dscale


def get_windows_locale():
    """
    Get Windows Locale

    Returns
    -------
    a string of Windows Locale
    """
    p = winps("(Get-Culture).Name")
    if p.returncode:
        raise Exception("Failed to get Windows Locale: ", p.stderr)
    win_locale = p.stdout.rstrip().replace("-", "_")
    return win_locale


def get_windows_theme():
    """
    Get Windows Theme

    Returns
    -------
    a string of either "light" or "dark"
    """
    raw_theme = registry("HKCU\\SOFTWARE\\Microsoft\\Windows\\Current"
                         "Version\\Themes\\Personalize", "AppsUseLightTheme")
    return "dark" if int(raw_theme, 0) else "light"


def get_windows_install_date(friendly_output=False):
    """
    Get the install date of the current installed build of Windows

    Parameters
    ----------
    friendly_output: bool
        whether the value returned is readable or not, `false` by default

    Returns
    -------
    A integer of unix timestamp or a string of readable time
    """
    raw_time = registry("HKLM\\Software\\Microsoft"
                        "\\Windows NT\\CurrentVersion", "InstallDate")
    dec_time = int(raw_time, 0)

    if friendly_output:
        from datetime import datetime
        f_time = \
            datetime.utcfromtimestamp(dec_time).strftime('%Y-%m-%d %H:%M:%S')
        return f_time
    else:
        return dec_time


def get_windows_branch():
    """
    Get the current Windows branch

    Returns
    -------
    a string of Windows Branch
    """
    raw_branch = registry("HKLM\\Software\\Microsoft"
                          "\\Windows NT\\CurrentVersion", "BuildBranch")
    return raw_branch


def get_windows_build(is_full_build=False):
    """
    Get Windows build information

    Parameters
    ----------
    is_full_vuild: bool
        if it should print full build, `False` by default

    Returns
    -------
    a string of windows build
    """
    if is_full_build:
        raw_build = registry("HKLM\\Software\\Microsoft"
                             "\\Windows NT\\CurrentVersion",
                             "BuildLabEx")
    else:
        raw_build = registry("HKLM\\Software\\Microsoft"
                             "\\Windows NT\\CurrentVersion",
                             "CurrentBuild")
    return raw_build


def get_windows_uptime():
    """
    Get the current up time in Windows

    Returns
    -------
    a array in the format of [days, hours, minutes]
    """
    p = winps("[int64]((get-date) - (gcim Win32_Operating"
              "System).LastBootUpTime).TotalSeconds")
    if p.returncode:
        return -1
    raw_time = int(p.stdout.rstrip())
    raw_days = raw_time // 86400
    raw_hours = raw_time // 3600 % 24
    raw_minutes = raw_time // 60 % 60
    return [raw_days, raw_hours, raw_minutes]

__all__ = ["get_current_executable", "get_display_scaling",
           "get_windows_locale", "get_windows_theme",
           "get_windows_install_date", "get_windows_branch",
           "get_windows_build", "get_windows_uptime",
           "registry", "distro_info"]
