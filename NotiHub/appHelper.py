# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

import threading

import NotiHub.services
from NotiHub import l
from NotiHub.services import __stub__


class serviceManger():
    class serviceInstant(threading.Thread):
        def __init__(self, serviceClass: __stub__.Service, config: __stub__.ConfigModel, id: int):
            super().__init__()

            self.service = serviceClass(config)
            self.meta = {
                "id": id,
                "is_api": self.service.config.isAPI,
                "type": self.service.__NAME__,
                "can_send": self.service.config.send,
                "can_receive": self.service.config.receive,
            }

        def run(self):
            self.service.connect()

        def stopListen(self):
            self.service.stopListen()

        def listen(self):
            self.service.listen()

    def __init__(self):
        self.services = []

    def create(self, service: __stub__.Service, config: __stub__.ConfigModel):
        if type(service) not in [str, object]: raise Exception("Invalid service")  # TODO CHECK
        if type(service) is str:
            if service in NotiHub.services.version:
                service = getattr(NotiHub.services, service)
            else:
                raise Exception("Could not find service: " + service)
        self.services.append(self.serviceInstant(service, config, len(self.services) + 1))
        l.debug("Created new service! ID: " + str(len(self.services)))

    def query(self, general: str = None, *, is_api: bool = None, can_send: bool = None, can_receive: bool = None,
              type: str = None):
        result = [service for service in self.services]
        if general:
            result = filter(lambda s: any(result in p for p in s.meta.values()), result)
        if is_api:
            result = filter(lambda s: s.meta["is_api"], result)
        if can_send:
            result = filter(lambda s: s.meta["can_send"], result)
        if can_receive:
            result = filter(lambda s: s.meta["can_receive"], result)
        if type:
            result = filter(lambda s: s.meta["type"].lower() == type.lower(), result)
        return list(result)

    def start(self):
        pass

    def startAll(self):
        [service.start() for service in self.services]

    def stop(self):
        pass

    def stopAll(self):
        pass

    def listen(self):
        pass

    def listenAll(self):
        [service.listen() for service in self.services]

    def silence(self):
        pass

    def silenceAll(self):
        [service.stopListen() for service in self.services]


class Config():
    def __init__(self, filename="notihub.cfg"):
        self.filename = filename
        self.load()

    def load(self):
        config = {}
        try:
            with open(self.filename, "r") as file:
                for line in file.readlines():
                    line = line.strip()
                    try:
                        if line:
                            if line[0] == '#': next
                            if line[0] == '[':
                                section = line[1:-1].lower()
                                if not section in config:
                                    config[section] = []
                                config[section].append({})
                            else:
                                key, val = line.split('=', 1)
                                key, val = key.strip().lower(), val.strip()
                                config[section][-1][key] = val if val.lower() not in ["y", "yes", "true", "n", "no",
                                                                                      "false"] else val[
                                                                                                        0].lower() > "q"  # HHAHA I'M SO LAZY
                    except Exception as e:
                        print("Error", str(e), " (line: %s)" % str(line))
        except FileNotFoundError:
            l.info(self.filename + " was not found, using defaults...")
            # TODO LOAD DEFAULTS
        self.services = {}
        for category in config:
            if category == "notihub":
                self.notihub = config["notihub"][0]
            elif category == "web":
                self.web = config["web"][0]
            elif category in NotiHub.services.version:
                self.services[category] = []
                for service in config[category]:
                    self.services[category].append(__stub__.ConfigModel(service))

    def save(self):
        raise Exception("Not Implemented")
        pass


import struct


class b91:
    # https://github.com/aberaud/base91-python/blob/master/base91.py
    # Base91 encode/decode for Python 2 and Python 3
    #
    # Copyright (c) 2012 Adrien Beraud
    # Copyright (c) 2015 Guillaume Jacquenot
    # All rights reserved.

    cipher = "n;:9xzNRr+oT$?_jeY>g6XBHfD[2y<FI3w*kQ8{^c}1\"sCuK(]M,Sv4LGt7ladW#Z5JU`E0O.p=%ihqm)@|P/&Ab!~V"
    cipher_table = dict((c, i) for i, c in enumerate(cipher))

    def decode(encoded_str):
        v = -1
        b = 0
        n = 0
        out = bytearray()
        for strletter in encoded_str:
            if not strletter in b91.cipher_table:
                continue
            c = b91.cipher_table[strletter]
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
        return out.decode("utf-8")

    """
    #
    # TODO Not going to encode passwords yet, will be used when I later implement a working web interface
    #
        def encode(source):
            source = source.encode()
            b = 0
            n = 0
            out = ''
            for count in range(len(source)):
                byte = source[count:count + 1]
                b |= struct.unpack('B', byte)[0] << n
                n += 8
                if n > 13:
                    v = b & 8191
                    if v > 88:
                        b >>= 13
                        n -= 13
                    else:
                        v = b & 16383
                        b >>= 14
                        n -= 14
                    out += b91.cipher[v % 91] + b91.cipher[v // 91]
            if n:
                out += b91.cipher[b % 91]
                if n > 7 or b > 90:
                    out += b91.cipher[b // 91]
            return out
    """
