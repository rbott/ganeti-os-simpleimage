# ganeti-os-simpleimage

A (very) simple image based OS provider for Ganeti

## Requirements

ganeti-os-simpleimage requires plain Python 3.6+ without any extra modules. However, you need `dd` for raw images and `qemu-img` for qcow2 images installed on your Ganeti machine. Currently this OS provider has only been tested in a KVM environment!

## Installation

As long as there are no official releases, you can simply do the following:

```shell
$ cd /usr/share/ganeti/os
$ git clone git@github.com:rbott/ganeti-os-simpleimage simple-image
```

Ganeti should automatically pick up the new OS provider and show a similar output to this:
```shell
$ gnt-os list
Name                       
debootstrap+default
simpleimage+qcow2
simpleimage+raw
```

## Usage

### Remote qcow2 Image

This example uses the official Debian 10 nocloud images:

```shell
$ gnt-instance add -o simpleimage+qcow2 \
    --os-parameters="source=http://cloud.debian.org/images/cloud/buster/20210129-530/debian-10-nocloud-amd64-20210129-530.qcow2" \
    -B memory=2G --disk 0:size=3G \
    --no-name-check --no-ip-check \
    debian-buster-nocloud
```

This will download and store the image locally. If add another instance, the image will not be downloaded again, unless the size of the remote file has changed.

### Local qcow2 Image

This example uses a Juniper vSRX image from the local disk:

```shell
$ gnt-instance add -o ganeti-os-simpleimage+qcow2 \
    --os-parameters="source=/var/lib/ganeti-os-simpleimage/junos-media-vsrx-x86-64-vmdisk-18.1R2.6.qcow2" \
    -B memory=4G --disk 0:size=17G \
    --no-name-check --no-ip-check \
    junos-vsrx-18.1
```

## Testing & Development

To run local unit tests, please install and use pytest:
```shell
$ python3 -m pytest
```
