#!/usr/bin/python3

import os

def get_blockdevice_size(device):
    """Return the size of the given blockdevice.

    Not the ideal solution, but does not need external modules.
    """
    fd = os.open(device, os.O_RDONLY)
    try:
        return os.lseek(fd, 0, os.SEEK_END)
    finally:
        os.close(fd)
