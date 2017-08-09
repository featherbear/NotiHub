# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

DEBUG = True
import builtins

builtins.dprint = lambda *args: print(*args) if DEBUG else None
import NotiHub.services
import NotiHub.web

def communicate(*args):
    print("\n\n\n\n"," ".join([*args]),"\n\n\n\n")
