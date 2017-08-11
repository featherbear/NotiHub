# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

class Grabber():
    __VERSION__ = ""
    __NAME__ = ""
    def __init__(self, apikey):
        self.apikey = apikey

    def connect(self, *_):
        raise Exception("Not implemented")

    def handler(self, *_):
        print("Stub Handler", *_)
        # raise Exception("Not implemented")