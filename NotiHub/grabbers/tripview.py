# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

??? [???]

The following code is licensed under the MIT License
"""

# __VERSION__ = "0.0.1"
#
# from .__stub__ import Grabber
# class grabber(Grabber):
#     def __init__(self, login, *, send, receive):
#         self.canSend = send
#         self.canReceive = receive
#         pass
#
#     def send(self, thread, data):
#         pass
#
#     def listen(self):
#         pass
#
#     def stopListen(self):
#         pass


"""


:: CityMapper
Oh gees. Their API only has three function (on the basic plan???) - nothing that is useful for me
Das' okay, a packet inspection on the CityMapper smartphone app reveals some pretty insightful information that we want.
Turns out that you can also retrieve the data on a website with your web browser; so integration will be easy
Thanks CityMapper!

-
INFO: https://citymapper.com/sydney/train/stations/SydneyStation_BexleyNorth


'''

# https://citymapper.com/api/1/departures?headways=1&ids=SydneyStop_BexleyRdAfterSladeRd_S&region_id=au-sydney
  Size: 3.82 KB
  More succint than /api/2/
  No live data still
  
# https://citymapper.com/api/2/departures?headways=1&ids=SydneyStop_BexleyRdAfterSladeRd_S&region_id=au-sydney
  Size: 5.05 KB

'''  # Buses

'''

# https://au-sydney-api.citymapper.com/1/departures?headways=1&ids=SydneyStation_BexleyNorth&cards=1&everythingmap=0
  Size: 3.20 KB
  Looks the best to me, has an array of times bound by their destination
# https://au-sydney-api.citymapper.com/2/departures?headways=1&ids=SydneyStation_BexleyNorth&cards=1&everythingmap=0
  Size: 7.57 KB
  Has a scheduled time, but no real time?

# https://citymapper.com/api/1/raildepartures?headways=1&ids=SydneyStation_BexleyNorth&region_id=au-sydney
# https://au-sydney-api.citymapper.com/1/raildepartures?ids=SydneyStation_BexleyNorth&cards=0&everythingmap=0
  Size: 43.6 KB
  Has abit more information + updated time
  
# https://citymapper.com/api/2/raildepartures?headways=1&ids=SydneyStation_BexleyNorth&region_id=au-sydney
# https://au-sydney-api.citymapper.com/2/raildepartures?ids=SydneyStation_BexleyNorth&cards=0&everythingmap=0
  Size: 22.7 KB
  Has a countdown - `time_seconds`
  Has platform information, as well as stations (and times) by trip
  NO LAST UPDATED TIME
  
'''  # Trains

"""  # CityMapper

# Config
# For each entry: GROUPTITLE! SERVICE:TRIPONE_DIRECTION[;TRIPTWO_DRECTION:TITLE] !, YALA MAJID
# GROUPTITLE is optional
# TITLE is optional
stops="SydneyStation_BexleyNorth:M41_1;400_0:"
# If ...Station then use api/2/raildepartures
# If ...Stop then use api/1/departures
# JSON Request
# Parse
_config = "Bexley North to Hurstville!SydneyStop_DATOTHERSIDE_S:491,SydneyStop_BexleyRdAfterSladeRd_S:M41!, SydneyStation_BexleyNorth:A:Bexley North to City"
if _config.count("!") % 2: raise Exception("Invalid config")
_config = _config.split("!,")
listing = []
def generateTrip(tripstring):
    # TODO offset
    triparr = tripstring.split(":")
    if len(triparr) == 1:
        raise Exception("Invalid config")
    return {
        'name':triparr[2].strip() if len(triparr) == 3 else '',
        'stop':triparr[1].strip(),
        'service':triparr[0].strip(),
    }
if len(_config)>1:
    # Means we have at least one group
    for item in _config:
        if "!" in item:
            # Then it's a group!
            groupname, trips = item.split("!")
            listing.append({
                'name': groupname.strip(),
                'trips': [generateTrip(trip) for trip in trips.split(",")]
            })
    else:
        listing.append(generateTrip(item))
print(listing)

import requests, json
def jsonUrl(url):
    with requests.get(url) as url: return json.loads(url.content.decode()) if url else {}
def busTrip(routeID, feed):
    route = list(filter(lambda route: route["name"] == routeID, feed["routes"]))
    if not route:
        print("Route `%s` not found" % routeID)
    else:
        route_id = route[0]["id"]
        #route[0]["long_name"]
        import itertools
        print(sorted(list(itertools.chain.from_iterable([item["next_departures"] for item in filter(lambda service: service["route_id"] == route_id, feed["services"])]))))


feed = jsonUrl("https://citymapper.com/api/1/departures?headways=1&ids=SydneyStop_BexleyRdAfterSladeRd_S&region_id=au-sydney")
name = feed["stops"][0]["name"]
code = feed["stops"][0]["stop_code"]
code = feed["stops"][0]["routes"]
busTrip("M41", feed["stops"][0])

from datetime import datetime

import requests


#

"""
'''
:: TripView
The TripView smartphone app makes calls to a backend hosted on the author's website (http://realtime.grofsoft.com/tripview/...)
Depending on what we request, we can get the start time for the trip, however this time is from stop/station 1; and I don't know if there's a way to request the times for a certain stop.
It does give us offsets (ie if the bus is early or late), but they're represented as `SCHEDULEDTIME,OFFSET`. That means we need to find the scheduled times for that particular bus stop and service - But that needs the NSW Transport GTFS database.. Which is BIG and slow..
We could download the database files TripView uses, but they're enc(rypted)oded; Unless we reverse engineer the libtdb.so library, we can't do that (plus it's breaking the ToS)

sooo not using TripView I guess

-
HEAD https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs
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
'''
import peewee
nswtransport_db = peewee.SqliteDatabase("nswtransport.db")
nswtransport_db.connect()
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

        '''
        for o in requests.get("http://realtime.grofsoft.com/tripview/realtime?routes=SB_M41_u&type=dv").json()['delays']:
            o = o['offsets'].split(",")
            l = {}
            t = datetime.now()
            T = [int(i) for i in o[-2].split(":")]
            if time(*T) >= time(t.hour, t.minute):
                print("Already passed")
            else:
                for a in range(0, len(o), 2):
                    l[o[a]] = o[a + 1]
                print(l)
        '''
"""  # TripView + NSW Transport
