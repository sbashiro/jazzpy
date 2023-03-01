# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Sergey Bashirov
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import re as _re
import requests as _requests


class Meeting:
    """Class representing the data of a single Jazz meeting"""

    def __init__(self, https_link: str, title: str = None):
        JAZZ_URL_PATTERN = r"https://(\S+)/(\S+)\?psw=(\S+)"
        match = _re.search(JAZZ_URL_PATTERN, https_link, _re.U | _re.I)
        groups = match.groups() if match else None

        if groups and len(groups) == 3:
            (self.server, self.id, self.password) = groups
        else:
            raise ValueError("Failed to parse URL: {}".format(https_link))

        self.title = title

    def __repr__(self):
        return repr(vars(self))

    def https_link(self) -> str:
        HTTPS_LINK = "https://{}/{}?psw={}"
        return HTTPS_LINK.format(self.server, self.id, self.password)

    def jazz_link(self) -> str:
        JAZZ_LINK = "jazz://join?id={}&password={}"
        return JAZZ_LINK.format(self.id, self.password)

    @staticmethod
    def create(title: str = None):
        if title is None:
            title = "Meeting"

        response = _requests.post("https://backend.jazz.sber.ru/room/create",
                                  json = {"roomTypeVersion": 1,
                                          "roomTitle": title,
                                          "roomType": "ANONYMOUS",
                                          "roomSettings": {"title": title,
                                                           "lobbyEnabled": False,
                                                           "sipEnabled": False},
                                          "guestEnabled": True},
                                  headers = {"Content-Type": "application/json; charset=utf-8",
                                             "Origin": "https://jazz.sber.ru",
                                             "Referer": "https://jazz.sber.ru",
                                             "x-client-authtype": "ANONYMOUS"})
        if response.status_code != 200:
            raise ConnectionError("{} {}".format(response.status_code, response.reason))

        return Meeting(response.json().get("url"), title)
