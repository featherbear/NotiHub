# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"
# from .__stub__ import Grabber

import feedparser
import re

def sanitize(string):
    return re.sub(r"(<script.*?>.*?<\/script>)","",string,flags=re.IGNORECASE)
    # (<([^biu])>)(.*?)(<\/\2>)

print(sanitize("<script></script>"))


# class grabber(Grabber):
class grabber():
    def __init__(self, feed=[], *feeds):
        self.urls = feed + [*feeds]

    def aggregate(self):
        feeds = [None if "bozo_exception" in feed else feed for feed in [feedparser.parse(feed) for feed in self.urls]]
        self.feeds = []
        for feed in feeds:
            obj = {
                "title": sanitize(["feed"]["title"]),
                "updated": feed['updated_parsed'],
                "posts": [],
            }
            [obj["posts"].append({
                "title": sanitize(entry["title"]),
                "updated": entry["published_parsed"],
                "url": entry["link"],
                "content": sanitize(entry["summary"])
            })
                for entry in feed["entries"]]
            self.feeds.append(obj)
        return self.feeds

    def send(self, thread, data):
        pass

    def listen(self):
        pass

    def stopListen(self):
        pass


v = grabber(["http://www.feedforall.com/sample.xml"])
print(v.aggregate())
