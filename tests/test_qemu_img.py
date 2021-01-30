#!/usr/bin/python3

from ganeti_os_simpleimage.qemu_img import *

def test_get_qcow2_real_size():
    qcow2_real_size = get_qcow2_real_size("tests/data/10MB.qcow2")
    assert 10485760 == qcow2_real_size