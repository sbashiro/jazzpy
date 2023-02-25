# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Sergey Bashirov
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import sys as _sys
import argparse as _argparse
import jazzpy as _jazzpy


def _print_message(message, file = None):
    if file is None:
        file = _sys.stdout
    file.write("{}\n".format(message))


def _print_error(message, file = None):
    if file is None:
        file = _sys.stderr
    file.write("{}: error: {}\n".format(_jazzpy.__title__, message))


def _parse_args():
    parser = _argparse.ArgumentParser(prog = _jazzpy.__title__,
                                      description = "Command line interface for Jazz.")
    parser.add_argument("--version", action = "version",
                        version = "{} {}".format(_jazzpy.__title__, _jazzpy.__version__))
    subparsers = parser.add_subparsers(title = "supported commands", dest = "command", required = True)

    convert_parser = subparsers.add_parser("convert", description = "Convert https link to jazz link.")
    convert_parser.add_argument("https_link", help = "meeting link from the Jazz app")

    schedule_parser = subparsers.add_parser("schedule", description = "Schedule a new meeting.")
    schedule_parser.add_argument("title", help = "meeting title")

    return parser.parse_args()


def _convert(args: _argparse.Namespace) -> int:
    try:
        meeting = _jazzpy.Meeting(args.https_link)
        _print_message(meeting.jazz_link())
        return 0
    except ValueError:
        _print_error("failed to convert link: {}".format(args.https_link))
        return 1


def _schedule_unimpl(args: _argparse.Namespace) -> int:
    _print_message(args.command)
    return 0


def _fail(args: _argparse.Namespace) -> int:
    _print_error("unimplemented command: {}".format(args.command))
    return 1


def main() -> int:
    args = _parse_args()
    command = globals().get("_{}".format(args.command), _fail)
    return command(args)
