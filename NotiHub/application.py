# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

import builtins
from NotiHub import *
from NotiHub.appHelper import *

print("Starting web server")
server = web.WebServer()
server.start()

NotiHub.communicate("communicate")
print(services.version)

config = Config()
services = serviceManger()
for servicetype in config.services:
    [services.create(servicetype,config) for config in config.services[servicetype]]
print(services.services)
services.startAll()
print("Connect start")
