#!/usr/bin/env python

#####
# Copyright (C) 2026  Fred Spreen
# Distributed under the terms of the GNU General Public License
#
# This file is part of StarbounderOffliner, a program to copy the Starbounder
# wiki into an OpenZIM file for offline perusal.
#
# StarbounderOffliner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# StarbounderOffliner is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# StarbounderOffliner. If not, see <https://www.gnu.org/licenses/>.
#####

import argparse
import logging
import os

_logger = logging.getLogger(__name__)

def main(args: argparse.Namespace) -> None:
    log_file_name: str = os.environ.get("PY_LOGFILE", "")

    if log_file_name:
        logging.basicConfig(
                filename = log_file_name,
                filemode = 'w',
                #DEFAULT: format = "%(levelname)s:%(name)s:%(message)s",
                format = "%(asctime)s %(name)s:%(levelname)s: %(message)s",
                level = os.environ.get("PY_LOG", "WARNING").upper()
                )
    else:
        logging.basicConfig(
                #DEFAULT: format = "%(levelname)s:%(name)s:%(message)s",
                format = "%(asctime)s %(name)s:%(levelname)s: %(message)s",
                level = os.environ.get("PY_LOG", "WARNING").upper()
                )


def instructions() -> None:
    print("ENVIRONMENT VARIABLES")
    print("  PY_LOGFILE - specify a file to write to (will be overwritten)")
    print("  PY_LOG     - log level to use (default 'WARNING')")
    print("               available levels are: debug, info, warning, error, critical")


if __name__ == "__main__":
    # see parameterList.ts
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--adminEmail", required=True, help="Email of the StarbounderOffliner operator. Will be put in the HTTP user-agent string for information only")
    arg_parser.add_argument("--pageList", help="List of pages to include.  Comma separated list of titles or a local path or HTTP(S) URL to a file with one title (in UTF8) per line")
    arg_parser.add_argument("--getCategories", action='store_true', help="Include the categories of all included pages.")
    args = arg_parser.parse_args()

    main(args)
