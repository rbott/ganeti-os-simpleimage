#!/usr/bin/python3

import subprocess
from sys import exit
import json

def run_qemu_img_with_json_output(mode, parameters):
    cmd = [
        "/usr/bin/qemu-img",
        mode,
        "--output=json",
    ]
    cmd = cmd + parameters
    try:
        qemu_img = subprocess.run(cmd, capture_output=True, check=True)
    except Exception as e:
        print("Failed to run '{}': {}".format(" ".join(cmd), e))
        exit(1)
    
    try:
        return json.loads(qemu_img.stdout)
    except Exception as e:
        print("Failed to parse JSON output from '{}': {}".format(" ".join(cmd), e))
        exit(1)


def run_qemu_img(parameters):
    cmd = [
        "/usr/bin/qemu-img"
    ]
    cmd = cmd + parameters
    try:
        qemu_img = subprocess.run(cmd, capture_output=True, check=True)
    except Exception as e:
        print("Failed to run '{}': {}\n{}".format(" ".join(cmd), e, e.stderr))
        exit(1)
    return qemu_img.stdout


def get_qcow2_real_size(image):
    info = run_qemu_img_with_json_output("info", [ image ])
    return info["virtual-size"]


def convert_qcow2_to_blockdevice(source, destination):
    print("Writing qcow2 image to blockdevice...", end="")
    run_qemu_img([
        "convert",
        "-f",
        "qcow2",
        "-O",
        "raw",
        source,
        destination
        ])
    print(" done")