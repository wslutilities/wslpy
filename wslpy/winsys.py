import subprocess

def __build__():
    buildcmd="reg.exe query \"HKLM\Software\Microsoft\Windows NT\CurrentVersion\" /v \"CurrentBuild\" 2>&1"
    p = subprocess.Popen(buildcmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output


def __branch__():
    branchcmd="reg.exe query \"HKLM\Software\Microsoft\Windows NT\CurrentVersion\" /v \"BuildBranch\" 2>&1"
    p = subprocess.Popen(branchcmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output

def __long_build__():
    longbuildcmd="reg.exe query \"HKLM\Software\Microsoft\Windows NT\CurrentVersion\" /v \"BuildLabEx\" 2>&1"
    p = subprocess.Popen(longbuildcmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    output = (routput.decode("utf-8").rstrip().split())[-1]
    return output

build=__build__()
branch=__branch__()
long_build=__long_build__()

