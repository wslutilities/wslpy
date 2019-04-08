import re
import subprocess
from enum import Enum


def __regInfoFetch__(key):
    cmd = u"reg.exe query \"HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output


def __regPathList__():
    cmd = u"reg.exe query \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\" /s"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    # Clean output first to toutput
    toutput = re.sub(
        r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\r\n", '', routput.decode('utf-8'))
    toutput = re.sub(r'(REG_EXPAND_SZ|\r|\n)', '', toutput)
    # split toutput into list with aoutput
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


def __regPathValue__(regname):
    try:
        regList = __regPathList__()
        if regname in regList.keys():
            return regList[regname]
        else:
            raise KeyError("Key does not exist in Registry.")
    except KeyError as err:
        print(err)


def __envInfoFetch__(key):
    cmd = u"powershell.exe query \"HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output


def reg_list():
    """
    List avaiable Registry keys to use and its corresponding path.

    Returns
    -------
    A Dictionary of registry keys and its corresbonding values.
    """
    return __regPathList__()


def from_reg(input):
    """
    Generate a path from a Registry Path Key.

    Parameters
    ----------
    input : str
        string of a registry Path Key.

    Returns
    -------
    A string of the corresbonding path from the input.

    Raises
    ------
    KeyError
        An error occured when you input a empty value or the registry key cannot be found in registry.
    """
    return __regPathValue__(input)
