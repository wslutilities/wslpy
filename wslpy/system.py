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
        string of a shell environment variable's location.

    Returns
    -------
    A string of the corresbonding value from the input.

    Raises
    ------
    KeyError
        An error occured when you input a empty value or the registry key cannot be found in registry.
    """
    return __shellEnvVar__(input)


def registry(input, key):

    #DUMMY CODE BEGINS (i am only using this to illustrate something)
    cmd = u"reg.exe query \""+input+"\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    #DUMMY CODE ENDS 

    # Given a valid registry path, retrieves the value of an entry in the registry.
    # Eg: registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","OS") returns "WINDOWS_NT"
    #
    # MAY return string type TODO: Doees this make sense?
    #
    # A valid registry path typically includes (this this and this)
    #
    # Parameters
    # ----------
    # input : str
    #     string of a shell environment variable key.
    #   
    #     Currently expected values: 
    #     "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" (for system)
    #     "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" (for shell)
    #     (Although any valid entries should work too) TODO: Check if required
    #
    # key : str 
    #     the name of the registry's key in string
    #
    # Returns
    # -------
    # The corresponding value TODO: Possibly type
    #
    # Raises
    # ------
    # Returns the error from Reg.exe (Possibly? )

    try:
        query = __regInfoFetch__(input, key)
        
        if query != "value.": #Error after regex #TODO: Check with Patrick on how he wants to handle this
            return query #Expected one
        else:
            raise KeyError("The following error propogated from Registry:" + routput.decode("utf-8").rstrip()) #TODO: 
    
    except KeyError as err:
        print(err)
 
#### Test Cases
#VALID 
# registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","OS")

#INVALID
registry("HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment","dasad")

#### Notes
# WILL BE DELETED

"""
for the current stage, it is expected to implement the feature provided by wslvar in wslu: https://github.com/wslutilities/wslu/blob/master/src/wslvar.sh

implement registry(input, key):
This function expect a registry path as input and the key item as key. The output should be its value; The optimal goal will be returning both the key
    type(Is it a string, a hex value, or something else?) and the key value in the proper format. This is currently being built with __regInfoFetch__(input, key)

"""