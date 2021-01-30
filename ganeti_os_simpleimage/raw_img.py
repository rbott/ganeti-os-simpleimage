#!/usr/bin/python3

import subprocess
from os import path

def get_raw_size(image):
    return path.getsize(image)

def write_raw_image_to_blockdevice(source, destination):
    cmd = [
        "/bin/dd",
        "if={}".format(source),
        "of={}".format(destination),
        "bs=1M"
    ]
    print("Writing raw image to blockdevice...", end="")
    try:
        dd = subprocess.run(cmd, capture_output=True, check=True)
    except Exception as e:
        print("Failed to run '{}': {}\n{}".format(" ".join(cmd), e, e.stderr))
        exit(1)
    print(" done")
    return dd.stderr
