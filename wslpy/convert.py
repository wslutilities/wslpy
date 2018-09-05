import re
import subprocess

def __regExec__(regname):
    cmd=u"reg.exe query \"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\\User Shell Folders\" /v \""+regname+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    # The following action is trying not to remove the space in the output result
    output = re.sub(r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\r\n", '', routput.decode('utf-8'))
    output = re.sub(regname, '', output, count=1)
    output = re.sub(r'REG_EXPAND_SZ', '', output)
    output = re.sub(r'^\s+(.+)\r\n\r\n$', r'\1', output)
    return output

def __Lin2Win__(path):
    # replace / to \
    path = re.sub(r'\/',r'\\', path)
    # replace \mnt\<drive_letter> to <drive_letter>:
    path = re.sub(r'\\mnt\\([A-Za-z])', r'\1:', path)
    return path

def __Win2Dwin__(path):
    # replace \ to \\
    return re.sub(r'\\', r'\\\\', path)

def __DWin2Lin__(path):
    # replace \\ to /
    path = re.sub(r'\\\\',r'\/', path)
    # replace <drive_letter>: to \mnt\<drive_letter>
    path = re.sub( r'([A-Za-z]):', r'\\mnt\\\1', path)
    return path