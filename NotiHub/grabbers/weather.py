# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the MIT License
"""

__VERSION__ = "0.0.1"
# from .__stub__ import Grabber

# class grabber(Grabber):
import feedparser
from bs4 import BeautifulSoup

class Grabber:
    def __init__(self, feed=[], *feeds):
        self.urls = feed + [*feeds]
        print("feeds",self.urls)
    def aggregate(self):
        self.feeds = [None if "bozo_exception" in feed else feed for feed in [feedparser.parse(feed) for feed in self.urls]]

class grabber(Grabber):
    def __init__(self):
        super().__init__(["http://rss.weatherzone.com.au/?u=12994-1285&lt=aploc&lc=1198&obs=1&fc=1&warn=1"])
        super().aggregate()
        print(self.feeds)
        self.feed = self.feeds[0]
        if not self.feed:
            print("ERROR!!!!")
        self.feedtime = self.feed["feed"]["published_parsed"]
        parser = BeautifulSoup(self.feed["entries"][0]["summary"],"html.parser")
        print(parser)
        print("\n\n\n----\n\n\n")
        parser = BeautifulSoup(self.feed["entries"][1]["summary"], "html.parser")
        print(parser)
grabber()
# http://www.bom.gov.au/catalogue/data-feeds.shtml
#   ftp://ftp.bom.gov.au/anon/gen/fwo/IDN11050.xml
#   http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94766.json
# https://openweathermap.org/price
# https://developer.accuweather.com/packages


# http://rss.weatherzone.com.au/?u=12994-1285&lt=aploc&lc=624&obs=1&fc=1&warn=1
# http://rss.weatherzone.com.au/?u=12994-1285&lt=aploc&lc=1198&obs=1&fc=1&warn=1

# http://api.accuweather.com/currentconditions/v1/22889.json?apikey=srRLeAmTroxPinDG8Aus3Ikl6tLGJd94&language=en-au&details=true&getphotos=false


# https://au-sydney-api.citymapper.com/1/weather?location=-33.967454,151.102757&ctxt=2&time=2017-08-15T16:55:46%2B10:00&units=c
# {"status": 0, "temperature": 18, "time": "2017-08-15T16:55:46+10:00", "units": "c", "icontype": "cloudy", "summary": "Overcast"}
"""
RSS is a free service offered by Weatherzone for use in RSS readers and for displaying weather information in websites.

You must use the RSS feeds as provided by Weatherzone, and you may not edit or modify the text, content or links supplied. The links back to Weatherzone included in the feed and the Weatherzone logo must be displayed when used in a website.

The feeds must not be used for any other purpose (including widgets and other applications) without the express permission of Weatherzone.

You must not query the feed any more frequently than once every 5 minutes for any given location. If using in a website you should implement caching to comply with this condition.

Breaching any of these terms may result in your IP address being blocked from the service
"""
