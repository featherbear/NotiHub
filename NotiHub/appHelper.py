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
