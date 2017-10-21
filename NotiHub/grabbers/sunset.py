# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the MIT License
"""

__VERSION__ = "0.0.1"
from .__stub__ import Grabber

from datetime import datetime, timedelta, timezone
from math import acos as AC, asin as AS, atan as AT, cos as C, floor as F, pi, sin as S, tan as T


# https://maas.museum/observations/2007/10/30/how-to-calculate-sunrise-and-set-a-worked-example/
class grabber(Grabber):
    def __init__(self, login, *, send, receive):
        self.canSend = send
        self.canReceive = receive
        pass

    @staticmethod
    def calculateSunTime(longitude: float, latitude: float, date: datetime = datetime.now(), zenith: float = 90.8):
        fr = lambda v, m: v + (m if v < 0 else (-m if v >= m else 0))
        day, month, year = (date.day, date.month, date.year)
        R = pi / 180
        N = F(275 * month / 9) - (F((month + 9) / 12) * (1 + F((year - 4 * F(year / 4) + 2) / 3))) + day - 30
        lh = longitude / 15
        t = (N + ((6 - lh) / 24)), (N + ((18 - lh) / 24))
        M = ((0.9856 * t) - 3.289 for t in t)
        l = tuple(fr(M + (1.916 * S(R * M)) + (0.020 * S(R * 2 * M)) + 282.634, 360) for M in M)
        ra = tuple(fr(1 / R * AT(0.91764 * T(R * L)), 360) for L in l)
        raQ = tuple((F(RA / 90)) * 90 for RA in ra)
        ra = tuple((ra[i] + (lQ - raQ[i])) / 15 for i, lQ in enumerate((F(L / 90)) * 90 for L in l))
        sd = (0.39782 * S(R * L) for L in l)
        deg = tuple((1 / R) * AC((C(R * zenith) - (sd * S(R * latitude))) / (C(AS(sd)) * C(R * latitude))) for sd in sd)
        gt = tuple(datetime(year, month, day, *hm).replace(tzinfo=timezone.utc).astimezone(
            tz=datetime.now().astimezone().tzinfo) for hm in
                   ((fr(int(UT), 24), int(round((UT - int(UT)) * 60, 0))) for UT in (fr(T - lh, 24) for T in (
                       H + ra[i] - (0.06571 * t[i]) - 6.622 for i, H in
                       enumerate(((360 - deg[0]) / 15, deg[1] / 15))))))
        return gt[0] - timedelta(days=1), gt[1]

[print(z[1].strftime("{} on %d/%m/%Y %H:%M".format(z[0]))) for z in zip(("Sunrise","Sunset"),service.calculateSunTime(151, -33))]
