from os import getcwd, environ
import subprocess


def __exec_command__(cmd, *, working_dir=None):
    """
    Execute a command in the shell and return the output.

    Parameters
    ----------
    cmd : str
        The command to be executed

    Returns
    -------
    The output of the command as a string

    Raises
    ------
    Returns the error from the command
    """
    if working_dir is None:
        working_dir = getcwd()
    try:
        cp = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=working_dir)
        if isinstance(cp.stdout, bytes):
            cp.stdout = cp.stdout.decode('utf-8')
        if isinstance(cp.stderr, bytes):
            cp.stderr = cp.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise Exception("command exec failed: ", e.stderr)
    else:
        return cp


def registry(input, key):
    """
    Given a valid registry path, retrieves the value of an entry in the
    registry.

    Parameters
    ----------
    input : str
        string of a shell environment variable key.

    key : str
        the name of the registry's key in string

    Returns
    -------
    The corresponding value as a string

    Raises
    ------
    Returns the error from Reg.exe
    """
    cmd = ["reg.exe", "query", input, "/v", key]
    p = __exec_command__(cmd)
    if p.returncode != 0:
        raise RuntimeError("The following error propagated from Registry: {}"
                           .format(p.stderr))

    query = p.stdout.rstrip()
    import re
    query = re.sub(r"^\r\n.+\r\n", "", query).lstrip()
    query = re.sub(key, "", query).lstrip()
    query = re.sub(r"REG_(SZ|MULTI_SZ|EXPAND_SZ|DWORD|BINARY|NONE)",
                   "", query).lstrip()
    return query


def distro_info(distro_name=None):
    """
    Returns the distro information as a string.

    Returns
    -------
    The distro information as a dictionary.

    Raises
    ------
    Returns the error from the command
    """
    if distro_name is None:
        if environ.get("WSL_DISTRO_NAME"):
            distro_name = environ.get("WSL_DISTRO_NAME")
        else:
            raise RuntimeError("WSL_DISTRO_NAME is not set")
    p = __exec_command__(["reg.exe", "query",
                          "HKCU\\SOFTWARE\\Microsoft\\"
                          "Windows\\CurrentVersion\\Lxss",
                          "/s", "/f", "DistributionName"])
    if p.returncode != 0:
        raise RuntimeError("failed to retrive distro information: {}"
                           .format(p.stderr))
    raw_data = p.stdout[2:]
    raw_list = raw_data.split("\r\n\r\n")[:-1]
    for raw_item in raw_list:
        if raw_item.endswith(distro_name):
            distro_loc = raw_item.split("\r\n")[0]
            p2 = __exec_command__(["reg.exe", "query", distro_loc, "/s"])
            if p2.returncode != 0:
                raise RuntimeError("failed to retrieve distro information: {}"
                                   .format(p2.stderr))
            import re
            raw_distro_info = p2.stdout
            # Clean output first to toutput
            out = re.sub((r"\r\nHKEY_CURRENT_USER.*\r\n"), '', raw_distro_info)
            # split toutput into list with aoutput
            out_p = (re.split(r'\s\s+', out))[1:][:-1]
            # convert aoutput to dictionary
            output = {item: {'type': type, 'value': value}
                      for item, type, value in zip(out_p[::3], out_p[1::3],
                                                   out_p[2::3])}
            return output
