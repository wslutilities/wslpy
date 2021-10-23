"""
This is the class that helps with wslu;
it is okay to use with other programs but it is not warranted
"""
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402


def findIcon(icon_name):
    """
    Find icon from a input string.

    Returns
    -------
    A path to the icon file, an empty string if not found.
    """
    icon_theme = Gtk.IconTheme.get_default()
    found_icon = ""
    for res in range(0, 512, 2):
        icon = icon_theme.lookup_icon(icon_name, res, 0)
        if icon:
            found_icon = icon.get_filename()
    return found_icon if found_icon else ""
