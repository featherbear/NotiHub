# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

Unofficial Facebook Chat API for Python [https://github.com/carpedm20/fbchat]
Unofficial Facebook Chat API [https://github.com/Schmavery/facebook-chat-api]

The following code is licensed under the GNU Public License Version v3.0
"""

import fbchat

from .__stub__ import Service

fbchat.log.disabled = True


class service(Service):
    __VERSION__ = "0.0.1"
    __NAME__ = "MESSENGER"

    class Messenger(fbchat.Client):
        def __init__(self, parent, *args):
            super().__init__(*args)
            parent.id = (parent.__NAME__, self.uid)
            self.dbWriter = parent.dbWriter

        def registerOnMessage(self, function):
            self.handler = function

        def onMessage(self, ts, thread_id, author_id, message, thread_type, **kwargs):
            if message:
                self.dbWriter(ts, thread_id, author_id, message)
                if self.uid != author_id: self.handler(
                    lambda thread_id, message: self.sendMessage(message, thread_id=thread_id, thread_type=thread_type),
                    ts, thread_id, author_id, message)

    def connect(self):
        self.messenger = self.Messenger(self, *self.config.getAuth())
        self.messenger.registerOnMessage(self.config.handler)
        self.listen()

    def send(self, thread, data):
        if self.config.send:
            thread_type = fbchat.ThreadType.GROUP if self.messenger.graphql_request(
                fbchat.GraphQL(doc_id='1386147188135407', params={
                    'id': thread,
                    'message_limit': 0,
                    'load_messages': False,
                    'load_read_receipts': False,
                    'before': None
                })).get("thread_type") == "GROUP" else fbchat.ThreadType.USER
            return self.messenger.sendMessage(data, thread_id=thread, thread_type=thread_type)

    def listen(self):
        if self.config.receive: self.messenger.listen()

    def stopListen(self):
        self.messenger.stopListening()
