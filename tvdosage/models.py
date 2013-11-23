#!/urs/bin/env python
#-*- coding: utf-8 -*-

import os

from peewee import Model, SqliteDatabase
from peewee import CharField, IntegerField, BooleanField
from playhouse.proxy import Proxy
from sqlite3 import OperationalError

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
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'database.db')
        database = SqliteDatabase(path)
        database_proxy.initialize(database)
    elif env == 'testing':
        database = SqliteDatabase(':memory:')
        database_proxy.initialize(database)
    #Try to create a Table but if it exist fail silenty
    Series.create_table(fail_silently=True)

def closedb():
	database_proxy.close()

