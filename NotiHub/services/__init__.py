# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

import builtins
import importlib
import pkgutil

if not hasattr(builtins, "dprint"): dprint = print

version = {}
dprint("Importing services")
for _, pyfilefull, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
    try:
        pyfile = pyfilefull[len(__name__) + 1:]
        if pyfile == "__stub__": continue
        dprint("  Importing " + pyfile)
        service = importlib.import_module(pyfilefull)
        service = service.service
        servicename = service.__NAME__.lower()
        try:
            version[servicename] = service.__VERSION__
        except AttributeError:
            version[servicename] = ""
        globals()[servicename] = service
    except Exception as e:
        dprint("    Error importing " + pyfile + " - " + str(e))
