#!/usr/bin/python3

from sys import exit
from os import path
import urllib.request
import urllib.parse
import posixpath
import shutil
import tempfile


def is_local_filepath(source):
    return source.startswith("/")


def is_http_url(source):
    return source.startswith("http://") or source.startswith("https://")


def is_accessible_file(source):
    return path.exists(source) and path.isfile(source)


def extract_filename(content_disposition_header, url):
    if content_disposition_header:
        filename = content_disposition_header.split("\"")[1]
    else:
        url_parsed = urllib.parse.urlparse(url)
        filename = path.basename(url_parsed.path)
    return filename


def is_download_required(image_url):
    req = urllib.request.Request(image_url, method="HEAD")
    r = urllib.request.urlopen(req)
    filename = "/tmp/{}".format(extract_filename(
        r.getheader('Content-Disposition'), r.geturl()))
    if not path.exists(filename):
        return True, filename

    remote_file_size = int(r.getheader('Content-Length'))
    local_file_size = path.getsize(filename)
    if remote_file_size == local_file_size:
        return False, filename
    else:
        return True, filename


def download_file(image_url, local_filename):
    download_location = tempfile.NamedTemporaryFile(delete=False)
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req) as in_stream, open(download_location.name, 'wb') as out_file:
        shutil.copyfileobj(in_stream, out_file)
    shutil.move(download_location.name, local_filename)


def acquire_image(source):
    if is_local_filepath(source):
        if not is_accessible_file(source):
            print("Error: '{}' does not exist or is not a regular file".format(source))
        return source
    elif is_http_url(source):
        print("Checking if a download is required...", end="")
        download_required, local_filename = is_download_required(source)
        print(" done")
        if download_required:
            print("Downloading {}...".format(source), end="")
            download_file(source, local_filename)
            print(" done")
        else:
            print("No new download required, file with the same name and size already exists locally")
        return local_filename

    else:
        print("Error: '{}' is neither a local absolute path nor a http(s) URL".format(source))
        exit(1)