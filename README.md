# ganeti-os-simpleimage

A (very) simple image based OS provider for Ganeti. It allows you to create an instance off a local image file or it can also download images through http(s) for you and cache them locally. Either raw or qcow2 images are supported. It does not interact in any way with the image (expanding filesystems, configuring users or IP addresses). This allows you to build and use your own templates/images or to install prebuild images like [Debian Cloud Images](http://cloud.debian.org/images/cloud/) or software distributed as disk images like Juniper vMX, vSRX or vQFX or Github Enterprise.

## Requirements

ganeti-os-simpleimage requires plain Python 3.6+ without any extra modules. However, you need `dd` for raw images and `qemu-img` for qcow2 images installed on your Ganeti machine. Currently this OS provider has only been tested in a KVM environment!

## Installation

As long as there are no official releases, you can simply do the following:

```shell
$ cd /usr/share/ganeti/os
$ git clone git@github.com:rbott/ganeti-os-simpleimage simple-image
```

Ganeti should automatically pick up the new OS provider and show output similar to this:
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

This will download and cache the image locally. If you add another instance, the image will not be downloaded again, unless the size of the remote file has changed.

### Local qcow2 Image

This example uses a Juniper vSRX image from the local disk:

```shell
$ gnt-instance add -o simpleimage+qcow2 \
    --os-parameters="source=/var/lib/ganeti-os-simpleimage/junos-media-vsrx-x86-64-vmdisk-18.1R2.6.qcow2" \
    -B memory=4G --disk 0:size=17G \
    --no-name-check --no-ip-check \
    junos-vsrx-18.1
```

You can access the local console of your JunOS instance using `gnt-instance console junos-vsrx-18.1`.

## Testing & Development

To run local unit tests, please install and use pytest:
```shell
$ python3 -m pytest
```
