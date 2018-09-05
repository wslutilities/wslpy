import re
import subprocess

def __regPathList__():
    cmd=u"reg.exe query \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\" /s"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()
    # Clean output first to toutput
    toutput = re.sub(r"\r\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders\r\n", '', routput.decode('utf-8'))
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