# -*- coding: utf-8 -*-

import pkgutil
import importlib

import builtins

if not hasattr(builtins, "dprint"): dprint = print

version = {}
dprint("Importing services")
for _, servicenamefull, _ in pkgutil.walk_packages(path=pkgutil.extend_path(__path__, __name__), prefix=__name__ + '.'):
    try:
        servicename = servicenamefull[len(__name__) + 1:]
        dprint("  Importing " + servicenamefull)
        service = importlib.import_module(servicenamefull)
        try:
            version[servicename] = service.__VERSION__
        except AttributeError:
            version[servicename] = ""
        globals()[servicename] = service.service
    except Exception as e:
        dprint("    Error importing " + servicenamefull + " - " + str(e))
