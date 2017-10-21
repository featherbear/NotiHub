# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the MIT License
"""

from NotiHub import *
from NotiHub.appHelper import *

l.info("Starting web server")

webserver = web.WebServer()
webserver.start()

config, services = Config(), serviceManger()
for servicetype in config.services:
    NotiHub.db.Service.get_or_create(name=servicetype)
    for config in config.services[servicetype]:
        services.create(servicetype, config)
services.startAll()

import NotiHub.genericWebCall
