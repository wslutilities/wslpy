import re
import subprocess
from enum import Enum

class PathConvType(Enum):
    """Types for Path Conversions"""

    """Automatic Conversion"""
    AUTO = 0

    """Convert to Linux Path"""
    LINUX = 1

    """Convert to Windows Path"""
    WIN = 2

    """Convert to Windows Path with Double Dash"""
    WINDOUBLE = 3


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
    path = re.sub(r'/',r'\\', path)
    # replace \mnt\<drive_letter> to <drive_letter>:
    path = re.sub(r'\\mnt\\([A-Za-z])', r'\1:', path)
    return path

def __Win2Dwin__(path):
    # replace \ to \\
    return re.sub(r'\\', r'\\\\', path)

def __DWin2Lin__(path):
    # replace \\ to /
    path = re.sub(r'\\\\',r'/', path)
    # replace <drive_letter>: to \mnt\<drive_letter>
    path = re.sub( r'([A-Za-z]):', r'/mnt/\1', path)
    return path

def reg_list():
    """
    List avaiable Registry keys to use and its corresponding path.
    
    :return: A Dictionary of registry keys and its corresbonding values.
    """
    return __regPathList__()

def from_reg(input):
    """
    Generate a path from a Registery Path Key.

    :param input: a Registery Path Key.
    :return: A string of the corresbonding path from the input.  
    :raise KeyError: An error occured when you input a empty value or the registery key cannot be found in registery.
    """
    return __regPathValue__(input)

def to_path(input, toType = PathConvType.AUTO):
    """
    Convert between 3 types of path used widely in WSL.

    :param input: the original path string.
    :param toType: Conversion Type. Uses convert.PathConvType. (Default: PathConvType.AUTO)
    :return: Converted path.
    :raise ValueError: An error occurred when the input is invalid.
    """
    try:
        if re.match(r'\/mnt\/[A-Za-z]', input) is not None: # Linux Path
            if toType == (PathConvType.AUTO or PathConvType.WIN):
                return __Lin2Win__(input)
            elif toType == PathConvType.LINUX:
                return input
            elif toType == PathConvType.WINDOUBLE:
                return __Win2Dwin__(__Lin2Win__(input))
            else:
                raise ValueError("Invalid Conversion Type "+toType)
        elif re.match(r'[A-Za-z]:\\\\', input) is not None: # Windows Path /w Double Dashline
            if toType == (PathConvType.AUTO or PathConvType.LINUX):
                return __DWin2Lin__(input)
            elif toType == PathConvType.WIN:
                return __Lin2Win__(__DWin2Lin__(input))
            elif toType == PathConvType.WINDOUBLE:
                return input
            else:
                raise ValueError("Invalid Conversion Type "+toType)
        elif re.match(r'[A-Za-z]:', input) is not None: # Windows Path
            if toType == (PathConvType.AUTO or PathConvType.LINUX):
                return __DWin2Lin__(__Win2Dwin__(input))
            elif toType == PathConvType.WIN:
                return input
            elif toType == PathConvType.WINDOUBLE:
                return __Win2Dwin__(input)
            else:
                raise ValueError("Invalid Conversion Type "+toType)
        else:
            raise ValueError("Invalid Path "+input)
    except ValueError as err:
        print(err)

