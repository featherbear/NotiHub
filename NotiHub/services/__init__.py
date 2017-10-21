# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the MIT License
"""

import importlib
import pkgutil
from NotiHub import l

version = {}
l.debug("Importing services")
for _, pyfilefull, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
    try:
        pyfile = pyfilefull[len(__name__) + 1:]
        if pyfile == "__stub__": continue
        l.debug("  Importing " + pyfile)
        service = importlib.import_module(pyfilefull)
        service = service.service
        servicename = service.__NAME__.lower()
        try:
            version[servicename] = service.__VERSION__
        except AttributeError:
            version[servicename] = ""
        globals()[servicename] = service
    except Exception as e:
        l.debug("    Error importing " + pyfile + " - " + str(e))
