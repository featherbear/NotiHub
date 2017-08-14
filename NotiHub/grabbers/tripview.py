# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"

from .__stub__ import Grabber
class grabber(Grabber):
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


from datetime import datetime

import requests

"""

https://api.tripview.com.au/config	GET	200	610b	215ms
https://api.tripview.com.au/svinfo?region=syd&version=3.5.6	GET	200	8.6kb	356ms
https://static.tripview.com.au/syd-401.zip	GET	200	1.8mb	3s
https://api.tripview.com.au/realtime?region=syd&routes=CR_eh_d&type=dtva	GET	200	921b	16s
https://api.tripview.com.au/realtime?region=syd&routes=CR_eh_u&type=dtva	GET	200	765b	22s
https://api.tripview.com.au/realtime?region=syd&routes=SB_M41_u&type=dtva	GET	200	135b	36s
https://api.tripview.com.au/realtime?region=syd&routes=SB_M41_d&type=dtva	GET	200	135b	36s
https://api.tripview.com.au/realtime?region=syd&routes=SB_491_d&type=dtva	GET	200	135b	51s
https://api.tripview.com.au/realtime?region=syd&routes=SB_491_u&type=dtva	GET	200	135b	52s
https://api.tripview.com.au/realtime?region=syd&routes=CR_eh_u%2CCR_il_d%2CCR_sc_d%2CCR_eh_d&type=dtva	GET	200	1.2kb	58s
https://api.tripview.com.au/realtime?region=syd&routes=CR_sc_u%2CCR_eh_d%2CCR_il_u&type=dtva	GET	200	688b	1min

"""

# HEAD https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs

import peewee

nswtransport_db = peewee.SqliteDatabase("nswtransport.db")

nswtransport_db.connect()

#
print("Checking for updated transport information...")
with requests.get("https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs",
                  headers={"Authorization": "apikey WUQ7i7CBYCQmlAf4uh8I5L7pjS9Zq5uZbNNF"}, stream=True) as gtfsSource:
    sourcetime = gtfsSource.headers["Last-Modified"]
    sourcetimestamp = int(datetime.strptime(sourcetime, '%a, %d %b %Y %H:%M:%S %Z').timestamp())
    if sourcetimestamp > nswtransport_db.pragma("user_version")[0]:
        print("New version: " + sourcetime)
        import os

        # with tempfile.TemporaryDirectory() as tempdir:
        tempdir = "D:\\LOL"
        gtfsZip = os.path.join(tempdir, "gtfs.zip")
        # with open(gtfsZip, 'wb') as f:
        #     print("Downloading")
        #     for chunk in gtfsSource.iter_content(chunk_size=1024):
        #         if chunk:  # filter out keep-alive new chunks
        #             f.write(chunk)
        print("Extracting")
        import zipfile
        #
        # with zipfile.ZipFile(gtfsZip, "r") as z:
        #     z.extractall(tempdir)

        gtfsFile = lambda filename, fields: playhouse.csv_loader.load_csv(nswtransport_db,
                                                                               os.path.join(tempdir, filename + ".txt"),
                                                                               fields=[field(default="") for field in fields])
        import playhouse.csv_loader

        print("Reading GTFS files")
        print("agency")
        gtfsFile("agency", [peewee.CharField] * 5 + [peewee.IntegerField])
        print("cal")
        gtfsFile("calendar", [peewee.CharField] + [peewee.BooleanField] * 7 + [peewee.DateField]*2)
        print("cal dates")
        gtfsFile("calendar_dates", [peewee.CharField, peewee.DateField, peewee.IntegerField])
        print("routes")
        gtfsFile("routes", [peewee.CharField] * 8)
        print("stops")
        gtfsFile("stops", [peewee.CharField] * 9)
        print("trips")
        gtfsFile("trips", [peewee.CharField] * 8)
        print("stoptimes")
        gtfsFile("stop_times",
                 [peewee.CharField] + [peewee.TimeField] * 2 + [peewee.IntegerField] * 2 + [peewee.CharField] + [
                     peewee.BooleanField] * 2 + [peewee.CharField])

        nswtransport_db.pragma("user_version", sourcetimestamp)
        print("Transport information updated")
# for o in requests.get("http://realtime.grofsoft.com/tripview/realtime?routes=SB_M41_u&type=dv").json()['delays']:
#     o = o['offsets'].split(",")
#     l = {}
#     t = datetime.now()
#     T = [int(i) for i in o[-2].split(":")]
#     if time(*T) >= time(t.hour, t.minute):
#         print("Already passed")
#     else:
#         for a in range(0, len(o), 2):
#             l[o[a]] = o[a + 1]
#         print(l)


# need to get stop times
