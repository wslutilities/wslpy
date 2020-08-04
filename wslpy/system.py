import re
import subprocess
from enum import Enum


def __shellEnvVarList__():
    cmd = u"reg.exe query \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\" /s"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    # Clean output first to toutput
    toutput = re.sub(
        r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\r\n", '', routput.decode('utf-8'))
    toutput = re.sub(r'(REG_EXPAND_SZ|\r|\n)', '', toutput)
    toutput = re.sub(r'(REG_SZ|\r|\n)', '', toutput)
    # split toutput into list with aoutput
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


def __shellEnvVar__(regname):
    try:
        shlList = __shellEnvVarList__()
        if regname in shlList.keys():
            return shlList[regname]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)


def __sysEnvVarList__():
    cmd = u"powershell.exe \"Get-ChildItem env:\""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    toutput = re.sub(r'(Name|Value|----|-|-----|\r|\n)',
                     '', routput.decode('utf-8'))
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


def __sysEnvVar__(varName):
    try:
        sysVarList = __sysEnvVarList__()
        if varName in sysVarList.keys():
            return sysVarList[varName]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)


def __regInfoFetch__(input, key):
    cmd = u"reg.exe query \""+input+"\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output


def __envInfoFetch__(key):
    cmd = u"powershell.exe query \"HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output


def shellEnvVarList():
    """
    List avaiable shell environment variables to use and its corresponding path.

    Returns
    -------
    A Dictionary of registry keys and its corresbonding values.
    """
    return __shellEnvVarList__()


def shellEnvVar(input):
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
        An error occured when you input a empty value or the registry key cannot be found in registry.
    """
    return __shellEnvVar__(input)


def sysEnvVarList():
    """
    List avaiable system environment variables to use and its corresponding path.

    Returns
    -------
    A Dictionary of system environement variables keys and its corresbonding values.
    """
    return __sysEnvVarList__()


def registry(input, key):
    """
    Get any value from registry provided the correct path.

    Returns
    -------
    A tuple of value type 'String','Int','Binary','HEX'or'null' and value of the queried registry.
    """
    keyValue = __regInfoFetch__(input, key)
    if re.match('0x', keyValue):
        keyType = 'HEX'
    elif re.match(r'^[10]*$', keyValue):
        keyType = 'Binary'
    elif re.match(r'^[A-Za-z0-9_\-\\: .;()]*$', keyValue):
        keyType = 'String'
    elif re.match(r'^[0-9]*$', keyValue):
        keyType = 'Int'
    else:
        keyType = 'null'
    return {keyType, keyValue}


def sysEnvVar(input):
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
        An error occured when you input a empty value or the registry key cannot be found in registry.
    """
    return __sysEnvVar__(input)
