import subprocess
from enum import Enum

def __regInfoFetch__(key):
    cmd=u"reg.exe query \"HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output

#: Returns Windows 10 Build number.
build=__regInfoFetch__("CurrentBuild")

#: Returns Windows 10 Branch information.
branch=__regInfoFetch__("BuildBranch")

#: Returns Windows 10 Long Build string.
long_build=__regInfoFetch__("BuildLabEx")

def CmdExec(command):
    """
    Execute cmd commands.
    
    :param command: cmd.exe commands.
    """
    cmd = u"cmd.exe /c \""+command+u"\""
    subprocess.call(cmd, shell=True)

def PwShExec(command):
    """
    Execute PowerShell(5.*) commands.
    :param command: powershell.exe commands.
    """
    cmd = u"powershell.exe -NoProfile -NonInteractive -Command \""+command+u"\""
    subprocess.call(cmd, shell=True)

def PwShCrExec(command):
    """
    Execute PowerShell Core 6 commands.
    :param command: pwsh.exe commands.
    """
    cmd = u"pwsh.exe -NoProfile -NonInteractive -Command \""+command+u"\""
    subprocess.call(cmd, shell=True)



