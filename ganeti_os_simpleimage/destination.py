#!/usr/bin/python3

import os

def get_blockdevice_size(device):
    fd = os.open(device, os.O_RDONLY)
    try:
        return os.lseek(fd, 0, os.SEEK_END)
    finally:
        os.close(fd)
