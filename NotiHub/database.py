# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the GNU Public License Version v3.0
"""

"""
[DATABASE]
    [ACCOUNTS]
        [PK]ID | [FK]SERVICES.ID
    [MESSAGES]
        [PK]ID | [FK]ACCOUNTS.ID | TIMESTAMP | THREAD | AUTHOR | DATA
    [SERVICES]
        [PK]ID | NAME
    [NICKNAMES]
        [PK]ID | [FK]ACCOUNTS.ID | PERSON | NICKNAME
"""

from peewee import *

notihub_db = SqliteDatabase("notihub.db")


class BaseModel(Model):
    class Meta:
        database = notihub_db


class Service(BaseModel):
    name = CharField(unique=True)


class Account(BaseModel):
    user = CharField()
    service = ForeignKeyField(Service, related_name="services")


class Nickname(BaseModel):
    account = CharField(unique=True)
    nickname = TextField()


class Message(BaseModel):
    timestamp = TimestampField()  # Or do we need to convert to datetime
    account = ForeignKeyField(Account, related_name="messages")
    author = CharField()
    thread = CharField()
    message = TextField()

    class Meta:
        order_by = ('-timestamp',)


class NotiHub_DB():
    Service = Service
    Account = Account
    Nickname = Nickname
    Message = Message

    def __init__(self):
        notihub_db.connect()
        notihub_db.create_tables([self.Service, self.Account, self.Nickname, self.Message], safe=True)
        self.peewee: SqliteDatabase = notihub_db

    def setNickname(self):
        pass

    def storeMessage(self, id, ts, thread_id, author_id, message):
        service = Service.get(name=id[0].lower())
        account = Account.get_or_create(user=id[1], service=service)[0]
        Message.create(account=account, timestamp=ts, thread=thread_id, author=author_id, message=message)


db = NotiHub_DB()
