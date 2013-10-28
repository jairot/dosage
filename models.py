#!/urs/bin/env python
#-*- coding: utf-8 -*-

from peewee import *

database = SqliteDatabase('database.db')
database.connect()

class CustomModel(Model):
    class Meta:
        database = database


class Series(CustomModel):
    name = CharField(unique = True)
    last_season = IntegerField(default = 1, null = True) 
    last_chapter = IntegerField(defautl = 1, null = True)
    tracking = BooleanField(default = False)
    junkie = BooleanField(default = False)
    quality =  CharField(default = "HDTV")
