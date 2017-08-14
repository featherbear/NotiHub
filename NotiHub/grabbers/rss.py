# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"
from .__stub__ import Grabber

import feedparser
class grabber(Grabber):
    def __init__(self, feed=[], *feeds):
        self.urls = feed + [*feeds]

    def aggregate(self):
        self.feed = [None if "bozo_exception" in feed else feed for feed in [feedparser.parse(feed) for feed in self.urls]]

    def send(self, thread, data):
        pass

    def listen(self):
        pass

    def stopListen(self):
        pass
