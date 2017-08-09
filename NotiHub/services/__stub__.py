# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""


class Service():
    __VERSION__ = ""
    __NAME__ = ""

    def __init__(self, *config):
        self.config = ConfigModel(*config)

    def connect(self):
        raise Exception("Not implemented")

    def send(self):
        raise Exception("Not implemented")

    def listen(self):
        raise Exception("Not implemented")

    def stopListen(self):
        raise Exception("Not implemented")

    def handler(self):
        raise Exception("Not implemented")


class ConfigModel():
    def __init__(self, obj: dict = None, *, login: str = None, password: str = None, send: bool = None,
                 receive: bool = None, handler=None):
        if type(obj) == dict:
            login = obj.get("email", obj.get("key"))
            password = obj.get("password", None)
            send = obj.get("send")
            if type(send) != bool: send = False
            receive = obj.get("receive")
            if type(receive) != bool: receive = False
            handler = obj.get("handler", lambda *_: None)

        self.isAPI = password is None
        self.login = login if ((not self.isAPI) and (login[0] == ".")) else login  # TODO "magic string manipulation"
        self.password = password if (
            (not self.isAPI) and (login[0] == ".")) else password  # TODO "magic string manipulation"
        self.send = send
        self.receive = receive
        self.handler = handler
        # TODO try import handler file, `handler` function
