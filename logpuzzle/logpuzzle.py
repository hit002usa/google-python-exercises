#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

from pathlib import Path

import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    hostname = 'http://' + Path(filename).name.split('_')[-1]
    url = r'GET\s(.+/puzzle/.+\.jpg)'

    with open(filename) as logfile:
        lines = logfile.readlines()

    urls = [hostname + re.search(url, l).group(1)
            for l in lines if re.search(url, l)]

    return sorted(list(set(urls)), key=lambda s: s.split('-')[-1])


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    dst = Path(dest_dir)
    dst.mkdir(parents=True, exist_ok=True)

    imgs_dst = str(dst.resolve()) + '/img'
    html_file = str(dst.resolve()) + '/index.html'

    image_tags = []

    for idx, url in enumerate(img_urls):
        print(f'Downloading image {url}')
        urllib.request.urlretrieve(url, f'{imgs_dst}{idx}.jpg')
        image_tags.append(f'<img src="{imgs_dst}{idx}.jpg">')
        print(f'Saved in {imgs_dst}{idx}.jpg')

    html = f"<html>\n<body>\n{''.join(image_tags)}\n</body>\n</html>"

    with open(html_file, 'w') as index:
        index.write(html)
        print('Created index.html to visualize images')


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
