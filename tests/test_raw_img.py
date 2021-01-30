#!/usr/bin/python3

from ganeti_os_simpleimage.raw_img import get_raw_size

def test_get_raw_size():
    sample_data_size = get_raw_size("tests/data/10bytes.data")
    assert 10 == sample_data_size