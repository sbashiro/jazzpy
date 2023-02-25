# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Sergey Bashirov
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import re as _re
import sys as _sys
import argparse as _argparse
from .__about__ import __version__


def _parse_args():
    parser = _argparse.ArgumentParser(prog = "jazzpy", description = "Command line interface for Jazz.")
    parser.add_argument("--version", action = "version", version = "%(prog)s {}".format(__version__))
    subparsers = parser.add_subparsers(title = "supported commands", dest = "command", required = True)

    convert_parser = subparsers.add_parser("convert", description = "Convert https link to jazz link.")
    convert_parser.add_argument("https_link", help = "meeting link from the Jazz app")

    schedule_parser = subparsers.add_parser("schedule", description = "Schedule a new meeting.")
    schedule_parser.add_argument("title", help = "meeting title")

    return parser.parse_args()


def _convert_unimpl(args: _argparse.Namespace) -> int:
    print(args.command)
    return 0


def _schedule_unimpl(args: _argparse.Namespace) -> int:
    print(args.command)
    return 0


def _fail(args: _argparse.Namespace) -> int:
    print("jazzpy: error: unimplemented command: {}".format(args.command))
    return 1


def main() -> int:
    args = _parse_args()
    command = globals().get("_{}".format(args.command), _fail)
    return command(args)
