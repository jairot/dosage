#!/urs/bin/env python
#-*- coding: utf-8 -*-

import os

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
    junky = BooleanField(default=False)
    quality = CharField(default="HDTV")


def startdb(env='production'):
    if env == 'production':
        home = os.path.expanduser("~")
        dosagepath = os.path.join(home, ".tvdosage/")
        if not os.path.exists(dosagepath):
            os.makedirs(dosagepath)
        path = os.path.join(dosagepath,
                            'database.db')
        database = SqliteDatabase(path)
    elif env == 'testing':
        database = SqliteDatabase(':memory:')
    database_proxy.initialize(database)
    #Try to create a Table but if it exist fail silenty
    Series.create_table(fail_silently=True)


def closedb():
    database_proxy.close()
