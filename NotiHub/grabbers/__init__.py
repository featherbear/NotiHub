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
l.debug("Importing grabbers")
for _, pyfilefull, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
    try:
        pyfile = pyfilefull[len(__name__) + 1:]
        if pyfile == "__stub__": continue
        l.debug("  Importing " + pyfile)
        grabber = importlib.import_module(pyfilefull)
        grabber = grabber.grabber
        grabbername = grabber.__NAME__.lower()
        try:
            version[grabbername] = grabber.__VERSION__
        except AttributeError:
            version[grabbername] = ""
        globals()[grabbername] = grabber
    except Exception as e:
        l.debug("    Error importing " + pyfile + " - " + str(e))
