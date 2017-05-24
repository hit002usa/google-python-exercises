#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Problem description:
# https://developers.google.com/edu/python/exercises/copy-special

from pathlib import Path
from zipfile import ZipFile

import shutil
import sys


"""Copy Special exercise"""


# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir):
    return [str(f) for f in Path(dir).resolve().iterdir()
            if f.is_file() and f.match('*__*__*')]


def copy_to(paths, dir):
    dst = Path(dir)
    dst.mkdir(parents=True, exist_ok=True)

    for special_files in paths:
        shutil.copy2(special_files, str(dst))


def zip_to(paths, dir):
    dst = Path(dir)
    name_file = 'temp.zip'

    if dst.name.endswith('.zip'):
        name_file = dst.name
        dst = dst.parents[0]

    dst.mkdir(parents=True, exist_ok=True)
    dst = dst / name_file

    print(f"Command I'm going to do:zip -j {dst}")
    with ZipFile(str(dst), 'w') as zip:
        for special_files in paths:
            print(f"{special_files}")
            zip.write(special_files)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

        copy_to(get_special_paths(args[0]), todir)

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

        zip_to(get_special_paths(args[0]), tozip)

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

        # +++your code here+++
        # Call your functions


if __name__ == "__main__":
    main()
