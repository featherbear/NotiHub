# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

pushbullet.py [https://github.com/randomchars/pushbullet.py]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"
import pushbullet


class service():
    def __init__(self, api_key, *, send, receive, device_iden=None):
        self.canSend = send
        self.canReceive = receive
        self.pushbullet = pushbullet.Pushbullet(api_key)
        self.listener = pushbullet.Listener(self.pushbullet, self._eventPush)
        self.device = None
        if device_iden:
            results = [d for d in self.pb.devices if d.device_iden == device_iden and d.active]
            self.device = results[0] if results else None
        self.last_push = 0

        if not self.device:
            try:
                device = self.pb.new_device("NotiHub")
                print("Created new device: NotiHub (id: %s)" % device.device_iden)
                self.device = device
            except:
                print("Error: Unable to create device")
                raise

    def _pushEvent(self, event):
        print(event)
        if event["type"] == "push" and event["push"]["type"] == "mirror":
            print("MIRROR")
        elif event["type"] == "tickle":
            print("TICKLE")
            self.check_pushes()

    def _pushFetch(self):
        pushes = self.pushbullet.get_pushes(self.last_push)
        for push in pushes:
            if not isinstance(push, dict):
                continue
            if ((push.get("target_device_iden", self.device.device_iden) == self.device.device_iden) and not (
                    push.get("dismissed", True))):
                self.handler(push.get("title", ""), push.get("body", ""))
                self.pushbullet.dismiss_push(push.get("iden"))
            self.last_push = max(self.last_push, push.get("created"))

    def send(self, data, title="", device=None):
        if self.canSend:
            return self.pushbullet.push_note(title, data, device=device)

    def listen(self):
        if self.canReceive:
            self.listener.run()

    def stopListen(self):
        self.listener.close()

    def handler(self, title, body):
        print(title)
        print(body)
