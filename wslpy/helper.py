import os
import re
import logging

from .core.check import get_mount_prefix, get_sys_drive_prefix
from .core.access import __exec_command__


def automount_drive(option=None, logging_level=logging.INFO):
    """
    This allows the automounting all other drives that will
    not automount using the defualt automount function.

    Parameters
    ----------
    option : str
        the options that will be used in the mount location.
        By default it will use the system defualt or your
        option in `wsl.conf`.
    logging_level : int
        the logging level that will be used. default is `logging.INFO`.
    """
    logging.basicConfig(level=logging_level)
    mntpnt_prefix = get_mount_prefix()
    sysdrv_prefix = get_sys_drive_prefix()
    logging.debug("mount prefix: {}  systemdrive prefix: {}"
                  .format(mntpnt_prefix, sysdrv_prefix))
    fsutil_path = os.path.join(sysdrv_prefix, "Windows",
                               "system32", "fsutil.exe")
    drv_p = __exec_command__([fsutil_path, "fsinfo", "drives"])
    if drv_p.returncode:
        err_str = "retrive Windows file system info failed: {}" \
                  .format(drv_p.stderr)
        logging.error(err_str)
        raise Exception(err_str)
    drv_list = drv_p.stdout.replace("\r\n", "") \
                           .replace(":", "") \
                           .replace("Drives ", "") \
                           .replace("\\", "") \
                           .lower().split()
    logging.debug("drive list: {}".format(str(drv_list)))

    if os.path.isfile("/etc/wsl.conf"):
        logging.debug("wsl.conf exists, checking it out")
        from configparser import ConfigParser
        c = ConfigParser()
        c.read("/etc/wsl.conf")
        if c.has_option("automount", "options"):
            option = c["automount"]["options"]
            logging.debug("got wsl.conf option: {}".format(option))

    if option is not None:
        # from subiquity.ayatem_setup.ui.views.wslconfbase
        # code written by me under AGPLv3 License
        # filesystem independent mount option
        fsimo = [r"async", r"(no)?atime", r"(no)?auto",
                 r"(fs|def|root)?context=\w+", r"(no)?dev", r"(no)?diratime",
                 r"dirsync", r"(no)?exec", r"group", r"(no)?iversion",
                 r"(no)?mand", r"_netdev", r"nofail", r"(no)?relatime",
                 r"(no)?strictatime", r"(no)?suid", r"owner", r"remount",
                 r"ro", r"rw", r"_rnetdev", r"sync", r"(no)?user", r"users"]
        # DrvFs filesystem mount option
        drvfsmo = r"case=(dir|force|off)|metadata|(u|g)id=\d+|(u|f|d)mask=\d+|"
        fso = "{0}{1}".format(drvfsmo, '|'.join(fsimo))

        if option != "":
            e_t = ""
            p = option.split(',')
            x = True
            for i in p:
                if i == "":
                    e_t += "an empty entry detected; "
                    x = x and False
                elif re.fullmatch(fso, i) is not None:
                    x = x and True
                else:
                    e_t += "{} is not a valid mount option; ".format(i)
                    x = x and False
            if not x:
                raise Exception("Invalid Input: {}Please check "
                                "https://docs.microsoft.com/en-us/windows/wsl/"
                                "wsl-config#mount-options "
                                "for correct valid input".format(e_t))
            for drv in drv_list:
                logging.debug("visiting drive %s" % drv)
                drv_path = os.path.join(mntpnt_prefix, drv)
                os.makedirs(drv_path, exist_ok=True)
                if not os.listdir(drv_path):
                    mount_p = __exec_command__(["mount", "-t", "drvfs",
                                                "{}:".format(drv.upper()),
                                                drv_path, "-o", option])
                    if mount_p.returncode:
                        logging.debug("failed to mount but still continue")
                        continue
