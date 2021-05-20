""" wslpy.internal

This is the class that helps working with wslu.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def findIcon(icon):
    """
    Find icon from a input string.

    Returns
    _______
    A path to the icon file, an empty string if not found.
    """
    return __findIcon__(icon)

def __findIcon__(icon_name):
    icon_theme = Gtk.IconTheme.get_default()
    found_icon = ""
    for res in range(0, 512, 2):
        icon = icon_theme.lookup_icon(icon_name, res, 0)
        if icon:
            found_icon = icon.get_filename()
    return found_icon if found_icon != "" else ""
