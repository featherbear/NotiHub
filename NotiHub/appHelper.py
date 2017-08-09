# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

import threading

import NotiHub.services
from NotiHub.services import __stub__


class serviceInstant(threading.Thread):
    def __init__(self, serviceClass, *options, **koptions):
        super().__init__()
        self.service: __stub__.Service = serviceClass(*options, **koptions)

    def run(self):
        self.service.connect()

    def stopListen(self):
        self.service.stopListen()

    def listen(self):
        self.service.listen()


class Config():
    filename = "notihub.cfg"

    def __init__(self):
        self.load()

    def load(self):
        print("load")
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
            print(self.filename, "was not found, using defaults...")
            # TODO LOAD DEFAULTS
        self.services = {}
        for category in config:
            print(category)
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
        return out

    def encode(bindata):
        b = 0
        n = 0
        out = ''
        for count in range(len(bindata)):
            byte = bindata[count:count + 1]
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
