# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"


# https://maas.museum/observations/2007/10/30/how-to-calculate-sunrise-and-set-a-worked-example/
class service():
    def __init__(self, login, *, send, receive):
        self.canSend = send
        self.canReceive = receive
        pass

    def send(self, thread, data):
        pass

    def listen(self):
        pass

    def stopListen(self):
        pass


import math

math.sind = lambda rad: math.sin(math.radians(rad))
math.cosecd = lambda rad: 1 / math.sind(rad)
math.acosd = lambda rad: math.degrees(math.acos(rad))
math.cosd = lambda rad: math.cos(math.radians(rad))
math.secd = lambda rad: 1 / math.cosd(rad)
math.tand = lambda rad: math.tan(math.radians(rad))


def stopListen(self):
    pass


import math

math.sind = lambda rad: math.sin(math.radians(rad))
math.cosecd = lambda rad: 1 / math.sind(rad)
math.cosd = lambda rad: math.cos(math.radians(rad))
math.secd = lambda rad: 1 / math.cosd(rad)
math.tand = lambda rad: math.tan(math.radians(rad))

# https://en.wikipedia.org/wiki/Sunrise_equation
"""
[Sun Declination]
C = -23.45° x cos(360/365 x (d+10)
:: d - day of the year < time.localtime().tm_yday >

[Hour Angle]
cos W = (sinA - sinBsinC)/cosBcosC
cos W = sinAsecBsecC - tanBtanC
W = cos^-1(sinAsecBsecC - tanBtanC)

:: A - altitude of the center of the solar disc to set about = -0.83° (-50 arcminutes)
:: B - latitude of the observer
:: C - declination of the sun
"""
