# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the MIT License
"""

DEBUG = False
import logging
logging.basicConfig(level=logging.INFO)
l = logging.getLogger("NotiHub")

import NotiHub.services
import NotiHub.web
from NotiHub.database import db

def communicate(*args):
    print(" ".join([*args]))
