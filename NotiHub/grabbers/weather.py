# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"


class service():
    def __init__(self, login, *, send, receive):
        self.canSend = send
        self.canReceive = receive
        pass

    def send(self, thread, data):
        pass

    def listen(self):
        pass

    def stopListen(self):
        pass
