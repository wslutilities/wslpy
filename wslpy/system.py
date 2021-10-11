import re
import subprocess


def shellEnvVarList():
    """
    List avaiable shell environment variables to use and
    its corresponding path.

    Returns
    -------
    A Dictionary of registry keys and its corresbonding values.
    """
    cmd = (u"reg.exe query \"HKCU\\Software\\Microsoft\\Windows"
           u"\\CurrentVersion\\Explorer\\User Shell Folders\" /s")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    # Clean output first to toutput
    toutput = re.sub((r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\"
                      r"Windows\\CurrentVersion\\Explorer\\User Shell"
                      r" Folders\r\n"), '', routput.decode('utf-8'))
    toutput = re.sub(r'(REG_EXPAND_SZ|\r|\n)', '', toutput)
    toutput = re.sub(r'(REG_SZ|\r|\n)', '', toutput)
    # split toutput into list with aoutput
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


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
        An error occured when you input a empty value or the registry key
        cannot be found in registry.
    """
    try:
        shlList = shellEnvVarList()
        if input in shlList.keys():
            return shlList[input]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)


def sysEnvVarList():
    """
    List avaiable system environment variables to use and
    its corresponding path.

    Returns
    -------
    A Dictionary of system environement variables keys and its corresbonding
    values.
    """
    cmd = u"powershell.exe \"Get-ChildItem env:\""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    toutput = re.sub(r'(Name|Value|----|-|-----|\r|\n)',
                     '', routput.decode('utf-8'))
    aoutput = (re.split(r'\s\s+', toutput))[1:]
    # convert aoutput to dictionary
    output = dict(zip(aoutput[::2], aoutput[1::2]))
    return output


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
        An error occured when you input a empty value or the registry key
        cannot be found in registry.
    """
    try:
        sysVarList = sysEnvVarList()
        if input in sysVarList.keys():
            return sysVarList[input]
        else:
            raise KeyError("Key does not exist.")
    except KeyError as err:
        print(err)
