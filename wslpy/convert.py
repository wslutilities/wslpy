""" wslpy.convert

This is the class that helps convert between 3 types of path used widely in WSL.
"""
import re
from enum import Enum


class PathConvType(Enum):
    """Types for Path Conversions

    `AUTO`
    Automatic Conversion

    `LINUX`
    Convert to Linux Path

    `WIN`
    Convert to Windows Path

    `WINDOUBLE`
    Convert to Windows Path with Double Dash
    """
    AUTO = 0
    LINUX = 1
    WIN = 2
    WINDOUBLE = 3


def __Lin2Win__(path):
    # replace / to \
    path = re.sub(r'/', r'\\', path)
    # replace \mnt\<drive_letter> to <drive_letter>:
    path = re.sub(r'\\mnt\\([A-Za-z])', r'\1:', path)
    return path


def __Win2Dwin__(path):
    # replace \ to \\
    return re.sub(r'\\', r'\\\\', path)


def __DWin2Lin__(path):
    # replace \\ to /
    path = re.sub(r'\\\\', r'/', path)
    # replace <drive_letter>: to \mnt\<drive_letter>
    path = re.sub(r'([A-Za-z]):', r'/mnt/\1', path)
    return path


def to(input, toType=PathConvType.AUTO):
    """
    Convert between 3 types of path used widely in WSL.

    Parameters
    ----------
    input : str
        the string of the original path.
    toType : PathConvType
        the type user wants to convert to. Default is PathConvType.AUTO.

    Returns
    -------
    string of converted path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    if re.match(r'\/mnt\/[A-Za-z]', input) is not None:  # Linux Path
        if toType == PathConvType.AUTO:
            return __Lin2Win__(input)
        elif toType == PathConvType.WIN:
            return __Lin2Win__(input)
        elif toType == PathConvType.LINUX:
            return input
        elif toType == PathConvType.WINDOUBLE:
            return __Win2Dwin__(__Lin2Win__(input))
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+toType)
    elif re.match(r'[A-Za-z]:\\\\', input) is not None:  # Windows Path /w Double Dashline
        if toType == PathConvType.AUTO:
            return __DWin2Lin__(input)
        elif toType == PathConvType.LINUX:
            return __DWin2Lin__(input)
        elif toType == PathConvType.WIN:
            return __Lin2Win__(__DWin2Lin__(input))
        elif toType == PathConvType.WINDOUBLE:
            return input
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+toType)
    elif re.match(r'[A-Za-z]:', input) is not None:  # Windows Path
        if toType == PathConvType.AUTO:
            return __DWin2Lin__(__Win2Dwin__(input))
        elif toType == PathConvType.LINUX:
            return __DWin2Lin__(__Win2Dwin__(input))
        elif toType == PathConvType.WIN:
            return input
        elif toType == PathConvType.WINDOUBLE:
            return __Win2Dwin__(input)
        else:
            raise ValueError("Invalid Conversion Type "+toType)
    else:
        raise ValueError("Invalid Path "+input)


def toWin(input):
    """
    Convert path to Windows style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Windows Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.WIN)


def toWinDouble(input):
    """
    Convert path to Windows Path /w Double style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Windows Path /w Double Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.WINDOUBLE)


def toWSL(input):
    """
    Convert path to Linux style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Linux Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.LINUX)
