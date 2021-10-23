"""
Provides users with the access for Windows system
information like system vatiables and registry keys.
"""
import re
from .__core__.access import __exec_command__
from wslpy.exec import winps
from .__core__.check import wsl_version, detect_distro


def list_shellenv():
    """
    List avaiable shell environment variables to use and
    its corresponding path.

    Returns
    -------
    A Dictionary of registry keys and its corresbonding values.
    """
    cmd = ["reg.exe", "query", "HKCU\\Software\\Microsoft\\Windows"
           "\\CurrentVersion\\Explorer\\User Shell Folders", "/s"]
    p = __exec_command__(cmd)
    if p.returncode != 0:
        raise RuntimeError("Failed to get shell environment variables: ",
                           p.stderr)
    routput = p.stdout
    # Clean output first to toutput
    toutput = re.sub((r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\"
                      r"Windows\\CurrentVersion\\Explorer\\User Shell"
                      r" Folders\r\n"), '', routput)
    toutput = re.sub(r'(REG_EXPAND_SZ|\r|\n)', '', toutput)
    toutput = re.sub(r'(REG_SZ|\r|\n)', '', toutput)
    # split toutput into list with aoutput
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


def get_shellenv(input):
    """
    Get the value from shell environment variable.

    Parameters
    ----------
    input : str
        string of a shell environment variable key.

    Returns
    -------
    A string of the corresbonding value from the input.

    Raises
    ------
    KeyError
        An error occured when you input a empty value or the registry key
        cannot be found in registry.
    """
    try:
        shlList = list_shellenv()
        if input in shlList.keys():
            return shlList[input]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)


def list_sysenv():
    """
    List avaiable system environment variables to use and
    its corresponding path.

    Returns
    -------
    A Dictionary of system environement variables keys and its corresbonding
    values.
    """
    p = winps("Get-ChildItem env:")
    if p.returncode != 0:
        raise RuntimeError("Failed to get system environment variables: ",
                           p.stderr)
    routput = p.stdout
    toutput = re.sub(r'(Name|Value|----|-|-----|\r|\n)',
                     '', routput)
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


def get_sysenv(input):
    """
    Get the value from shell environment variable.

    Parameters
    ----------
    input : str
        string of a shell environment variable key.

    Returns
    -------
    A string of the corresbonding value from the input.

    Raises
    ------
    KeyError
        An error occured when you input a empty value or the registry key
        cannot be found in registry.
    """
    try:
        sysVarList = list_sysenv()
        if input in sysVarList.keys():
            return sysVarList[input]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)


def get_ip():
    """
    Get the current IPv4 address from your WSL2 instance

    Returns
    -------
    A string of IPv4 address
    """
    import netifaces as ni
    return ni.ifaddresses("eth0")[ni.AF_INET][0]['addr']


__all__ = [
    "list_shellenv",
    "get_shellenv",
    "list_sysenv",
    "get_sysenv",
    "wsl_version",
    "detect_distro",
    "get_ip",
    ]
