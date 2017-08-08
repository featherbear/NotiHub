import threading
from NotiHub.services import __init__, __stub__
import os.path


class serviceInstant(threading.Thread):
    def __init__(self, serviceClass, *options, **koptions):
        super().__init__()
        self.service: __stub__.Service = serviceClass(*options, **koptions)

    def run(self):
        self.service.connect()

    def stopListen(self):
        self.service.stopListen()

    def listen(self):
        self.service.listen()


class Config():
    filename = "notihub.cfg"
    def __init__(self):
        self.load()
    def load(self):
        file = open(self.filename)
        self.lol = ""
        config = {}
        for line in file.readlines():
            line = line.strip()
            try:
                if line:
                    if line[0] == '#': next
                    if line[0] == '[':
                        section = line[1:-1]
                        if not config.has_key(section):
                            config[section] = {}
                    else:
                        (key, val) = line.split('=', 1)
                        if not config[section].has_key(key):
                            config[section][key] = []
                        config[section][key].append(val)
            except Exception as e:
                print(str(e)," (line: %s)" % str(line))
        print(config)

        for servicename in __init__.version:
            service : __stub__.Service = getattr(__init__, servicename)
            service._NAME
            service._AUTHMETHOD
        #return config
    def save(self):
        pass