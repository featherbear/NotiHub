# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

pushbullet.py [https://github.com/randomchars/pushbullet.py]

The following code is licensed under the MIT License
"""

import pushbullet

from .__stub__ import Service

pushbullet.Pushbullet._push_ = pushbullet.Pushbullet._push
pushbullet.Pushbullet._push = lambda self, data: self._push_(
    {**data, "source_device_iden": self.device_iden} if hasattr(self, "device_iden") else data)


class service(Service):
    __VERSION__ = "0.0.1"
    __NAME__ = "PUSHBULLET"

    def connect(self):
        self.pushbullet = pushbullet.Pushbullet(*self.config.getAuth())
        self.id = (self.__NAME__, self.uid)
        self.listener = pushbullet.Listener(self.pushbullet,
                                            lambda event: (self._pushFetch() if event["type"] == "tickle" else None))

        self.device = ([d for d in self.pushbullet.devices if d.nickname == "NotiHub"] + [None])[0]
        if not self.device:
            try:
                self.device = self.pushbullet.new_device("NotiHub")
                print("Created new device: NotiHub (id: %s)" % self.device.device_iden)
            except:
                print("Error: Unable to create device")
                raise
        self.last_push = 0
        self.listen()

    def _pushFetch(self):
        pushes = self.pushbullet.get_pushes(self.last_push)
        for push in pushes:
            if not isinstance(push, dict):
                continue

            # Get only pushes directed to the NotiHub device - Do we want to keep this function?
            if ((push.get("target_device_iden", self.device.device_iden) == self.device.device_iden) and not (
                    push.get("dismissed", True))):
                title = push.get("title", "")
                message = str(len(title)) + "\x00" + title + push.get("body", "")
                """
                Title: HELLO
                Body: Example
                
                Parsing message: "5\x00HELLOExample"
                    _divider = message.index("\x00")
                    titleLength = int(message[:_divider])
                    (title,body) = (message[_divider+1:_divider+1+titleLength], message[_divider+1+titleLength:])
                """
                self.dbWriter(push.get("created"), push.get("sender_iden", "unknown"),
                              push.get("source_device_iden", ""), message)
                self.pushbullet.dismiss_push(push.get("iden"))
                self.config.handler(push)

            self.last_push = max(self.last_push, push.get("created"))

    def send(self, data, title="NotiHub", device=None):
        if self.config.send:
            return self.pushbullet.push_note(title, data, device=(
                type('s', (), {"device_iden": device}) if type(device) == str else device))

    def listen(self):
        if self.config.receive:
            self.listener.run()

    def stopListen(self):
        self.listener.close()
