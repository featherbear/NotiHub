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

    def connect(self, *_):
        raise Exception("Not implemented")

    def send(self, *_):
        raise Exception("Not implemented")

    def listen(self, *_):
        raise Exception("Not implemented")

    def stopListen(self, *_):
        raise Exception("Not implemented")

    def handler(self, *_):
        print("Stub handler")
        print(*_)
        raise Exception("Not implemented")


import importlib
import struct

cipher = "n;:9xzNRr+oT$?_jeY>g6XBHfD[2y<FI3w*kQ8{^c}1\"sCuK(]M,Sv4LGt7ladW#Z5JU`E0O.p=%ihqm)@|P/&Ab!~V"
cipher_table = dict((c, i) for i, c in enumerate(cipher))

def b91d(encoded_str):
    v = -1
    b = 0
    n = 0
    out = bytearray()
    for strletter in encoded_str:
        if not strletter in cipher_table:
            continue
        c = cipher_table[strletter]
        if (v < 0):
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            while True:
                out += struct.pack('B', b & 255)
                b >>= 8
                n -= 8
                if not n > 7:
                    break
            v = -1
    if v + 1:
        out += struct.pack('B', (b | v << n) & 255)
    return out


class ConfigModel():
    def __init__(self, obj: dict = None, *, login: str = None, password: str = None, send: bool = None,
                 receive: bool = None, handler=None):
        if type(obj) == dict:
            login = obj.get("email", obj.get("key"))
            assert type(login) is not None
            password = obj.get("password", None)
            send = obj.get("send")
            if type(send) != bool: send = False
            receive = obj.get("receive")
            if type(receive) != bool: receive = False
            handler = obj.get("handler")

        self.isAPI = password is None
        self.isProtected = login.startswith("--")
        self.login = login
        self.password = password
        self.send = send
        self.receive = receive
        try:
            self.handler = importlib.import_module("NotiHub.handler." + handler)
        except (TypeError, ModuleNotFoundError):
            self.handler = Service.handler

    def getAuth(self):
        if self.isAPI:
            return self.login
        if self.isProtected:
            return b91d(self.login[2:]), b91d(self.password[2:])
        else:
            return self.login, self.password
