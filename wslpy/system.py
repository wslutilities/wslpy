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
    # INTERNAL FUNCTION
    #
    # Note: We would normally expect err to propagate the result if there is one like so 
    # q = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # aoutput,erra = q.communicate()
    # print(erra)
    #
    # However Python does not seem to yet be capable to capture this error, thus the workaround you'll see
    #
    # Parameters
    # ----------
    # input : str
    #     string of a shell environment variable key.
    #   
    #
    # key : str 
    #     the name of the registry's key in string
    #
    #
    # Returns
    # -------
    # The corresponding result, pre-formatted depending on type
    #
    # Raises
    # ------
    # Returns the error from Reg.exe in string

    cmd = u"reg.exe query \""+input+"\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    

    #A WORKAROUND TILL AN UPSTREAM FIX IS MADE
    if routput[0:9] == b'\r\n\r\nERROR': #Expected: ERROR: The system was unable to find the specified registry key or value.
        return routput.decode("utf-8","unicode_escape") #TODO: CHECK IF OTHER ERRORS APPEAR IN TEST SUITE
    else:
        return routput.decode("utf-8","unicode_escape").rstrip().split() #This is an array that contains this ['HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session', 'Manager\\Environment', 'OS', 'REG_SZ', 'Windows_NT']



def __envInfoFetch__(key):
    cmd = u"reg.exe query \"HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\" /v \""+key+u"\" 2>&1"
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


def registry(input, key, show_type=False):
    """
    Given a valid registry path, retrieves the value of an entry in the registry, and type if requested.
    Eg: registry("HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment","OS") returns "WINDOWS_NT"

    A valid registry path typically looks like:
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment" (for system)
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" (for shell)
        (Although any valid entries should work too)

    Parameters
    ----------
    input : str
        string of a shell environment variable key.
    
    key : str 
        the name of the registry's key in string

    show_type : bool
        if show_type = True, registry() will also return the type of variable used. show_type is False otherwise
        and by default

    Returns
    -------
    The corresponding value as a string, an array in the form [value,type] otherwise

    Raises
    ------
    Returns the error from Reg.exe 
    """

    query = __regInfoFetch__(input, key)
    
    if type(query) == list: 
        if show_type:
            return [query[4],query[3]]
        else:
            return query[4] #Expected one
    else:
        raise RuntimeError("The following error propogated from Registry: " + query) 


    #### Test Cases
    #VALID 
    #registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","OS")
    #print(registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","OS",show_type=True))
    #print(registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","OS"))

    #INVALID
    #print(registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","dasad"))
    #__regInfoFetch__("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","dasad")


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
