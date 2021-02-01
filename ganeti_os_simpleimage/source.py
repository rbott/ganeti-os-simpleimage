#!/usr/bin/python3

from sys import exit
from os import path
import urllib.request
import urllib.parse
import shutil
import tempfile


def is_local_filepath(filepath):
    """Determine if the given path is a local path."""
    return filepath.startswith("/")


def is_http_url(filepath):
    """Determine if the given path is a http(s) URL."""
    return filepath.startswith("http://") or filepath.startswith("https://")


def is_accessible_file(filepath):
    """Determine if the given path exists and is a regular file."""
    return path.exists(filepath) and path.isfile(filepath)


def extract_filename(content_disposition_header, url):
    """Extract the filename from the Content-Disposition
    HTTP Header (if present) - or use the last part of the URL.

    Error out if the extracted string is empty.
    """
    if content_disposition_header:
        filename = content_disposition_header.split("\"")[1]
        # sanitize filename from Content-Disposition header
        filename = path.basename(filename)
    else:
        url_parsed = urllib.parse.urlparse(url)
        filename = path.basename(url_parsed.path)
    if not filename:
        print("Error: could neither generate a valid filename from Content-Disposition header nor from download URL.")
        exit(1)
    return filename


def is_download_required(image_url):
    """Determine if a fresh download is required.

    Either because the file is not yet there or because
    the size of the file has changed on the remote server.
    """

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
    """Perform the HTTP(S) download of the given URL."""
    download_location = tempfile.NamedTemporaryFile(delete=False)
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req) as in_stream, open(download_location.name, 'wb') as out_file:
        shutil.copyfileobj(in_stream, out_file)
    shutil.move(download_location.name, local_filename)


def acquire_image(source):
    """Return the filename of the image to write to the target device.
    
    Takes care of the download if the file is stored remotely.
    """
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