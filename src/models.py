#!/urs/bin/env python
#-*- coding: utf-8 -*-

from peewee import Model, SqliteDatabase
from peewee import CharField, IntegerField, BooleanField

from playhouse.proxy import Proxy

database_proxy = Proxy()


class CustomModel(Model):
    class Meta:
        database = database_proxy


class Series(CustomModel):
    name = CharField(unique=True)
    last_season = IntegerField(default=1, null=True)
    last_chapter = IntegerField(defautl=1, null=True)
    tracking = BooleanField(default=False)
    junkie = BooleanField(default=False)
    quality = CharField(default="HDTV")


def startdb(env='production'):
    if env == 'production':
        database = SqliteDatabase('database.db')
        database_proxy.initialize(database)
    elif env == 'testing':
        database = SqliteDatabase(':memory:')
        database_proxy.initialize(database)
        Series.create_table()
