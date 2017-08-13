# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"


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


class GTFSModel(peewee.Model):
    class Meta:
        database = nswtransport_db


class Agency(GTFSModel):
    # "X0000","NSW TrainLink","http://transportnsw.info","Australia/Sydney","EN","131500"
    agencyID = peewee.CharField(unique=True)
    agencyName = peewee.CharField()


class Calendar(GTFSModel):
    # "TA+r1359+1","0","0","0","1","1","0","0","20170810","20171108"
    serviceID = peewee.CharField(unique=True)
    monday = peewee.BooleanField()
    tuesday = peewee.BooleanField()
    wednesday = peewee.BooleanField()
    thursday = peewee.BooleanField()
    friday = peewee.BooleanField()
    saturday = peewee.BooleanField()
    sunday = peewee.BooleanField()
    dateStart = peewee.DateField()
    dateEnd = peewee.DateField()


class CalendarDate(GTFSModel):
    # "TA+r1034+1","20170810","2"
    # ???
    serviceID = peewee.ForeignKeyField(Calendar, related_name="dates")
    date = peewee.DateField()
    exceptionType = peewee.CharField()


class Route(GTFSModel):
    # "2-BMT-sj2-1","X0000","","Blue Mountains Line","Intercity Trains Network","2","F6891F","FFFFFF"
    routeID = peewee.CharField(unique=True)
    agency = peewee.ForeignKeyField(Agency, related_name="routes")
    shortName = peewee.CharField()
    longName = peewee.CharField()
    description = peewee.CharField()
    type = peewee.CharField()


class Trip(GTFSModel):
    # "2-BMT-sj2-1","TA+r1034+1","2.TA.2-BMT-sj2-1.1.H","2-BMT-sj2-1.1.H","Springwood Station","0","1+2","1"
    tripID = peewee.CharField()
    routeID = peewee.ForeignKeyField(Route, related_name="trips")
    serviceID = peewee.ForeignKeyField(Calendar, related_name="trips")
    headsign = peewee.CharField()
    direction = peewee.BooleanField()
    blockID = peewee.CharField()


class Stop(GTFSModel):
    # "228055","228055","Pacific Hwy After Murray St","-33.0036096083102","151.685565693411","","","0",""
    stopID = peewee.CharField(unique=True)
    name = peewee.CharField()
    platform = peewee.CharField()


class StopTime(GTFSModel):
    # "1.TA.2-BMT-sj2-1.1.H", "07:52:01", "07:52:01", "2000338", "1", "", "0", "1", "0"
    tripID = peewee.ForeignKeyField(Calendar, related_name="times")
    stopID = peewee.ForeignKeyField(Stop, related_name="times")
    time = peewee.TimeField()


models = [Agency, Calendar, CalendarDate, Route, Trip, Stop, StopTime]

nswtransport_db.connect()

#
import csv

#

#
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

        with zipfile.ZipFile(gtfsZip, "r") as z:
            z.extractall(tempdir)


        class gtfsFile(object):
            def __init__(self, filename):
                self.csv = csv.reader(open(os.path.join(tempdir, filename + ".txt")), delimiter=',')
                next(self.csv, None)

            def __enter__(self):
                return self.csv

            def __exit__(self, *_):
                pass


        print("Dropping and creating tables")
        nswtransport_db.drop_tables(models)
        nswtransport_db.create_tables(models)
        print("Reading GTFS files")
        with gtfsFile("agency") as agency, \
                gtfsFile("calendar") as calendar, \
                gtfsFile("calendar_dates") as calendar_dates, \
                gtfsFile("routes") as routes, \
                gtfsFile("stop_times") as stop_times, \
                gtfsFile("stops") as stops, \
                gtfsFile("trips") as trips:
            print("Populating agencies")
            [Agency.create(agencyID=row[0], agencyName=row[1]) for row in agency]
            print("Populating calendar #1")
            [Calendar.create(serviceID=row[0], monday=row[1], tuesday=row[2], wednesday=row[3], thursday=row[4],
                             friday=row[5], saturday=row[6], sunday=row[7], dateStart=row[8], dateEnd=row[9]
                             ) for row in calendar]
            print("Populating calendar #2")
            [CalendarDate.create(serviceID=row[0], date=row[1], exceptionType=row[2]) for row in calendar_dates]
            print("Populating routes")
            [Route.create(routeID=row[0], agency=row[1], shortName=row[2], longName=row[3], description=row[4],
                          type=row[5]
                          ) for row in routes]
            print("Populating stops")
            [Stop.create(stopID=row[0], name=row[2], platform=row[-1]) for row in stops]
            print("Populating trips")
            [Trip.create(tripID=row[2], routeID=row[0], serviceID=row[1], headsign=row[4], direction=row[5],
                         blockID=row[6]
                         ) for row in trips]
            print("Populating timetable")
            [StopTime.create(tripID=row[0], stopID=row[3], time=row[1]) for row in stop_times]

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
