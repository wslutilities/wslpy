"""wslpy.library
"""
import subprocess

def detectDistro():
    distro = subprocess.getoutput(
        "head -n1 /etc/os-release | sed -e 's/NAME=\"//;s/\"//'")
    return distro