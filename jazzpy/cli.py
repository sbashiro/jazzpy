# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Sergey Bashirov
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import sys as _sys
import os.path as _path
import argparse as _argparse
import requests as _requests
import toml as _toml
import jazzpy as _jazzpy


_HISTORY_SIZE_MAX = 256
_HISTORY_FILE_NAME = _path.expanduser(_path.join("~", ".{}.toml".format(_jazzpy.__title__)))


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

    show_parser = subparsers.add_parser("show", description = "Show last scheduled meeting.")
    show_parser.add_argument("--all", action = "store_true", help = "list all history")

    return parser.parse_args()


def _load_history():
    history = {}

    if _path.exists(_HISTORY_FILE_NAME):
        try:
            history = _toml.load(_HISTORY_FILE_NAME)
        except _toml.TomlDecodeError as e:
            _print_error("{}: {}".format(_HISTORY_FILE_NAME, str(e)))

    return history.get("meeting", [])


def _save_history(history):
    try:
        with open(_HISTORY_FILE_NAME, mode = "w") as file:
            _toml.dump({"meeting": history}, file)
    except OSError as e:
        _print_error(str(e))


def _add_to_history(meeting):
    history = _load_history()
    history.insert(0, meeting.toml_dict())

    if len(history) > _HISTORY_SIZE_MAX:
        history.pop()

    _save_history(history)


def _convert(args: _argparse.Namespace) -> int:
    meeting = _jazzpy.Meeting(args.https_link)
    _print_message(meeting.jazz_link())
    return 0


def _schedule(args: _argparse.Namespace) -> int:
    meeting = _jazzpy.Meeting.create(args.title)
    _print_message(meeting.format())
    _add_to_history(meeting)
    return 0


def _show(args: _argparse.Namespace) -> int:
    history = _load_history()

    if not args.all:
        history = history[0:1]

    for params in history:
        _print_message(_jazzpy.Meeting(**params).format())

    return 0


def _fail(args: _argparse.Namespace) -> int:
    _print_error("unimplemented command: {}".format(args.command))
    return 1


def main() -> int:
    args = _parse_args()
    command = globals().get("_{}".format(args.command), _fail)

    try:
        return command(args)
    except Exception as e:
        _print_error(str(e))
        return 1
