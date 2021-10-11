import subprocess


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

    cmd = u"reg.exe query \""+input+"\" /v \""+key+u"\" 2>&1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    routput, err = p.communicate()

    # A WORKAROUND TILL AN UPSTREAM FIX IS MADE
    # Expected: ERROR: The system was unable to find the specified registry
    # key or value.
    if routput[0:9] == b'\r\n\r\nERROR':
        # TODO: CHECK IF OTHER ERRORS APPEAR IN TEST SUITE
        query = routput.decode("utf-8", "unicode_escape")
    else:
        # This is an array that contains this
        # ['HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session',
        #   'Manager\\Environment', 'OS', 'REG_SZ', 'Windows_NT']
        query = routput.decode("utf-8", "unicode_escape").rstrip().split()

    if type(query) == list:
        if show_type:
            return [query[4], query[3]]
        else:
            return query[4]  # Expected one
    else:
        raise RuntimeError(
            "The following error propogated from Registry: " + query)
