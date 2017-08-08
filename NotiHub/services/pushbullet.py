# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

pushbullet.py [https://github.com/randomchars/pushbullet.py]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"
import pushbullet
from .__stub__ import Service

pushbullet.Pushbullet._push_ = pushbullet.Pushbullet._push
pushbullet.Pushbullet._push = lambda self, data: self._push_(
    {**data, "source_device_iden": self.device_iden} if hasattr(self, "device_iden") else data)


class service(Service):
    _NAME = "PUSHBULLET"
    _AUTHMETHOD = Service.TYPE_API
    def connect(self):
        self.pushbullet = pushbullet.Pushbullet(self.authorisation)
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
                self.handler(push.get("created"), push.get("title", None), push.get("body", None))
                self.pushbullet.dismiss_push(push.get("iden"))

            self.last_push = max(self.last_push, push.get("created"))

    def send(self, data, title="NotiHub", device=None):
        if self.canSend:
            return self.pushbullet.push_note(title, data, device=(
                type('s', (), {"device_iden": device}) if type(device) == str else device))

    def listen(self):
        if self.canReceive:
            self.listener.run()

    def stopListen(self):
        self.listener.close()

