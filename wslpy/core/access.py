from os import getcwd
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


def registry(input, key, show_type=False):
    """
    Given a valid registry path, retrieves the value of an entry in the
    registry, and type if requested.
    Eg: registry("HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control
              \\Session Manager\\Environment","OS") returns "WINDOWS_NT"

    A valid registry path typically looks like:
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\
            Session Manager\\Environment" (for system)
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\
            User Shell Folders" (for shell)
        (Although any valid entries should work too)

    Parameters
    ----------
    input : str
        string of a shell environment variable key.

    key : str
        the name of the registry's key in string

    show_type : bool
        if show_type = True, registry() will also return the type of variable
        used. show_type is False otherwise
        and by default

    Returns
    -------
    The corresponding value as a string, an array in the form [value,type]
    otherwise

    Raises
    ------
    Returns the error from Reg.exe
    """
    cmd = ["reg.exe", "query", input, "/v", key]
    p = __exec_command__(cmd)
    if p.returncode != 0:
        raise RuntimeError("The following error propogated from Registry: {}"
                           .format(p.stderr))
    routput = p.stdout

    # This is an array that contains this
    # ['HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session',
    #   'Manager\\Environment', 'OS', 'REG_SZ', 'Windows_NT']
    query = routput.rstrip().split()

    if show_type:
        return [query[4], query[3]]
    else:
        return query[4]  # Expected one
