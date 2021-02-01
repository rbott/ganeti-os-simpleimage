#!/usr/bin/python

from os import environ
from os import path
from sys import exit

EXPECTED_OS_PARAMETERS = [
    "source",
]

ALLOWED_OS_VARIANTS = [
    "raw",
    "qcow2"
]

def get_disk_param(disk_id, param_name):
    env_var_name = "DISK_{}_{}".format(disk_id, param_name)
    if env_var_name in environ:
        return environ[env_var_name]
    else:
        return ""


def parse_environment():
    config = {
        'instance_name': '',
        'hypervisor': '',
        'variant': '',
        'parameters': {},
        'disks': []
    }

    for key, value in environ.items():
        if key == "INSTANCE_NAME":
            config["instance_name"] = value
        elif key == "HYPERVISOR":
            config["hypervisor"] = value
        elif key == "OS_VARIANT":
            config["variant"] = value
        elif key == "DISK_COUNT":
            disk_count = int(value)
            for i in range(disk_count):
                disk = {
                    "id": i,
                    "uuid": get_disk_param(i, "UUID"),
                    "path": get_disk_param(i, "PATH"),
                    "type": get_disk_param(i, "BACKEND_TYPE"),
                    "access": get_disk_param(i, "ACCESS")
                }
                config["disks"].append(disk)
        elif key.startswith("OSP_"):
            param_name = key.split("_", 1)[1]
            config["parameters"][param_name.lower()] = value
            
    return config


def verify_base_parameters(config):
    if not config["instance_name"]:
        print("Error: instance_name is empty")
        exit(1)
    
    if config["hypervisor"] != "kvm":
        print("Error: only KVM is currently supported (cluster is using '{}'".format(config["hypervisor"]))
        exit(1)

    if not config["variant"]:
        print("Error: OS variant not specified")
        exit(1)


def verify_disk_parameters(disks):
    for disk in disks:
        if not disk["path"]:
            print("Error: disk {} has no path set".format(disk["id"]))
            exit(1)

        if not path.exists(disk["path"]):
            print("Error: path/device {} for disk {} does not exist".format(disk["path"], disk["id"]))
        
        if not disk["type"]:
            print("Error: disk {} has no type set".format(disk["id"]))
            exit(1)


def verify_os_parameters(params):
    for param in EXPECTED_OS_PARAMETERS:
        if param not in params:
            print("Error: OS parameter '{}' not provided".format(param))


def verify_config(config):
    verify_base_parameters(config)
    verify_disk_parameters(config["disks"])
    verify_os_parameters(config["parameters"])
