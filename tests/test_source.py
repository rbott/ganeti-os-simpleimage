#!/usr/bin/python3

from ganeti_os_simpleimage.source import *

def test_is_local_filepath():
    valid_paths = [
        "/tmp/test.img",
        "/"
    ]
    invalid_paths = [
        "d",
        "invalidpath"
        "https://www.ganeti.org",
    ]

    for path in valid_paths:
        check = is_local_filepath(path)
        assert True == check
    
    for path in invalid_paths:
        check = is_local_filepath(path)
        assert False == check


def test_is_http_url():
    valid_urls = [
        "http://www.ganeti.org",
        "https://www.ganeti.org"
    ]

    invalid_urls = [
        "",
        "/"
        "/tmp/test.img",
    ]

    for url in valid_urls:
        check = is_http_url(url)
        assert True == check
    
    for url in invalid_urls:
        check = is_http_url(url)
        assert False == check


def test_is_accessible_file():
    accessible_file = "tests/data/10bytes.data"
    inaccessible_file = "tests/data/missingfile"

    check = is_accessible_file(accessible_file)
    assert True == check

    check = is_accessible_file(inaccessible_file)
    assert False == check


def test_extract_filename():
    filename_with_header = extract_filename("attachement; filename=\"image.img\"", "https://www.ganeti.org/folder/missleading.img")
    filename_without_header = extract_filename(None, "https://www.ganeti.org/folder/image.img")

    assert "image.img" == filename_with_header
    assert "image.img" == filename_without_header

