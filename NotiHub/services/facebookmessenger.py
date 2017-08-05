# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

Unofficial Facebook Chat API for Python [https://github.com/carpedm20/fbchat]
Unofficial Facebook Chat API [https://github.com/Schmavery/facebook-chat-api]

The following code is licensed under the GNU Public License Version v3.0
"""

__VERSION__ = "0.0.1"
import fbchat


class service():
    class Messenger(fbchat.Client):
        def onMessage(self, message, author_id, thread_id, thread_type, ts, **kwargs):
            pass

    def __init__(self, email, password, *, send, receive):
        self.canSend = send
        self.canReceive = receive
        self.messenger = self.Messenger(email, password)

    def send(self, thread, data):
        if self.canSend:
            thread_type = 2 if self.messenger.graphql_request(fbchat.GraphQL(doc_id='1386147188135407', params={
                'id': thread,
                'message_limit': 0,
                'load_messages': False,
                'load_read_receipts': False,
                'before': None
            })).get("thread_type") == "GROUP" else 1
            return self.sendMessage(data, thread_id=thread, thread_type=thread_type)

    def listen(self):
        if self.canReceive: self.messenger.listen()

    def stopListen(self):
        self.messenger.stopListening()


        ## client.isLoggedIn()
        ## client.logout()
        # onLoggedIn
