#!/usr/bin/python3

from ganeti_os_simpleimage.destination import get_blockdevice_size

def test_get_blockdevice_size():
    sample_data_size = get_blockdevice_size("tests/data/10bytes.data")
    assert 10 == sample_data_size
