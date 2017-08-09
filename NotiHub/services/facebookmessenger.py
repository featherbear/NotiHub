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


class service(Service):
    __VERSION__ = "0.0.1"
    __NAME__ = "MESSENGER"

    class Messenger(fbchat.Client):
        def registerOnMessage(self, function):
            self.handler = function

        def onMessage(self, message, author_id, thread_id, thread_type, ts, **kwargs):
            self.handler(ts, thread_id, author_id, message)

    def connect(self):
        self.messenger = self.Messenger(self.config.login, self.config.password)
        self.messenger.registerOnMessage(self.config.handler)
        self.listen()

    def send(self, thread, data):
        if self.canSend:
            thread_type = 2 if self.messenger.graphql_request(fbchat.GraphQL(doc_id='1386147188135407', params={
                'id': thread,
                'message_limit': 0,
                'load_messages': False,
                'load_read_receipts': False,
                'before': None
            })).get("thread_type") == "GROUP" else 1
            return self.messenger.sendMessage(data, thread_id=thread, thread_type=thread_type)

    def listen(self):
        if self.canReceive: self.messenger.listen()

    def stopListen(self):
        self.messenger.stopListening()


        ## client.isLoggedIn()
        ## client.logout()
        # onLoggedIn
