#!/usr/bin/python3

import subprocess
from sys import exit
import json

def run_qemu_img_with_json_output(mode, parameters):
    """Helper function to run qemu-img with output as JSON"""
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
    """Helper function to run qemu-img with arbitrary parameters."""
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
    """Run qemu-img to get the size of the (expanded) qcow2 image."""
    info = run_qemu_img_with_json_output("info", [ image ])
    return info["virtual-size"]


def convert_qcow2_to_blockdevice(source, destination):
    """Run qemu-img to convert a qcow2 to raw."""
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