"""
This is the class that helps convert between
3 types of path used widely in WSL.
"""
import re
from enum import Enum
from .__core__.check import get_mount_prefix


class PathType(Enum):
    """Types for Path Conversions

    `AUTO`
    Automatic Conversion

    `LINUX`
    Convert to Linux Path

    `WIN`
    Convert to Windows Path

    `WIN_DOUBLE`
    Convert to Windows Path with Double Dash
    """
    AUTO = 0
    LINUX = 1
    WIN = 2
    WIN_DOUBLE = 3


def __post_mount_prefix__():
    a = get_mount_prefix()
    a = re.sub(r"^\/", r"", a)
    a = re.sub(r"\/$", r"", a)
    return a


MOUNT_PREFIX = __post_mount_prefix__()


def __lin2win__(path, is_ns_modern=False):
    if re.match(r'^/{}'.format(MOUNT_PREFIX), path) is not None:
        # replace / to \
        path = re.sub(r'/', r'\\', path)
        converted_mount = re.sub(r'/', r'\\', MOUNT_PREFIX)
        # replace \<mount_location>\<drive_letter> to <drive_letter>:
        path = re.sub(r'\\{}\\([A-Za-z])'.format(converted_mount),
                      r'\1:', path)
    else:
        from os import environ
        if not environ.get('WSL_DISTRO_NAME'):
            raise Exception(
                "WSL_DISTRO_NAME env not found. unable to convert.")
        # remove trailing /
        path = re.sub(r'^/', r'', path)
        # replace / to \
        path = re.sub(r'/', r'\\', path)
        # replace /<mount_location>/<drive_letter> to <drive_letter>:
        type_name = "wsl$"
        if is_ns_modern:
            type_name = "wsl.localhost"
        path = "\\\\{}\\{}\\{}".format(type_name,
                                       environ.get('WSL_DISTRO_NAME'),
                                       path)
    return path


def __win2dwin__(path):
    # replace \ to \\
    return re.sub(r'\\', r'\\\\', path)


def __dwin2lin__(path):
    # replace \\ to /
    path = re.sub(r'\\\\', r'/', path)
    # replace <drive_letter>: to /<mount_location>/<drive_letter>
    path = re.sub(r'([A-Za-z]):', r'/{}/\1'.format(MOUNT_PREFIX), path)
    return path


def to(input, to_type=PathType.AUTO, is_ns_modern=False):
    """
    Convert between 3 types of path used widely in WSL.

    Parameters
    ----------
    input : str
        the string of the original path.
    to_type : PathType
        the type user wants to convert to. Default is PathType.AUTO.
    is_ns_modern : bool
        if the linux path needs to convert to new style(``wsl.localhost``).
        Default is False (``wsl$``).

    Returns
    -------
    string of converted path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    # Windows Path /w Double Dash-line
    if re.match(r'^[A-Za-z]:\\\\', input) is not None:
        if to_type in (PathType.AUTO, PathType.LINUX):
            return __dwin2lin__(input)
        elif to_type == PathType.WIN:
            return __lin2win__(__dwin2lin__(input), is_ns_modern)
        elif to_type == PathType.WIN_DOUBLE:
            return input
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+to_type)
    elif re.match(r'^[A-Za-z]:', input) is not None:  # Windows Path
        if to_type in (PathType.AUTO, PathType.LINUX):
            return __dwin2lin__(__win2dwin__(input))
        elif to_type == PathType.WIN:
            return input
        elif to_type == PathType.WIN_DOUBLE:
            return __win2dwin__(input)
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+to_type)
    elif re.match(r'^\\\\wsl', input) is not None:  # WSL Windows Path
        # \\wsl$\\<distro_name>\\<path> is the original style path;
        # \\wsl\\<distro_name>\\<path> is the new style path but deprecated;
        # \\wsl.localhost\\<distro_name>\\<path> is the current new style path.
        input = re.sub(r'^\\\\(wsl|wsl\$|wsl\.localhost)\\[^\\]*\\',
                       r'\\', input)
        input = re.sub(r'\\', r'/', input)
        if to_type in (PathType.AUTO, PathType.LINUX):
            return input
        elif to_type == PathType.WIN:
            return __lin2win__(input, is_ns_modern)
        elif to_type == PathType.WIN_DOUBLE:
            return __win2dwin__(__lin2win__(input, is_ns_modern))
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+to_type)
    # Linux Path
    else:
        if to_type in (PathType.AUTO, PathType.WIN):
            return __lin2win__(input)
        elif to_type == PathType.LINUX:
            return input
        elif to_type == PathType.WIN_DOUBLE:
            return __win2dwin__(__lin2win__(input, is_ns_modern))
        else:
            raise ValueError("ERROR: Invalid Conversion Type "+to_type)


def to_win(input):
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
    return to(input, PathType.WIN)


def to_win_double(input):
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
    return to(input, PathType.WIN_DOUBLE)


def to_wsl(input):
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
    return to(input, PathType.LINUX)
