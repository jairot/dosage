#!/urs/bin/env python
#-*- coding: utf-8 -*-
"""This Module works as a Dosage Runner"""

import argparse

from models import *

parser = argparse.ArgumentParser()
parser.add_argument("--track", help = "Start tracking the given tv series")
parser.add_argument("--untrack", help = "Stop tracking the given tv series")
parser.add_argument("--junky", help = "Put the given tv series on Junky mode")

#    name = CharField(unique = True)
#    last_season = IntegerField(default = 1, null = True) 
#    last_chapter = IntegerField(defautl = 1, null = True)
#    tracking = BooleanField(default = False)
#    junkie = BooleanField(default = False)
#    quality =  CharField(default = "HDTV")

def track(name, season = 1, chapter = 1):
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        serie =  Series.create(name = name, last_season = season, 
                        last_chapter= chapter, tracking = True)
    else:
        serie.tracking = True
        serie.save()
    print "Tracking %s"%name
   

def untrack(name):
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        print "You are not Tracking that Tv Series"
    else:
        serie.tracking = False
        serie.save()
        print "Untracking %s"%name

def junky(name, season = 1, chapter = 1):
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        serie =  Series.create(name = name, last_season = season, 
                        last_chapter= chapter, tracking = True, junkie = True)
    else:
        serie.tracking = True
        serie.junkie = True
        serie.save()
    finally:
        #No more than 1 tv series in junky mode at the time
        series = Series.select().where(Series.name != name, Series.junkie == True)
        for serie in series:
            serie.junkie =  False
            serie.save()
            print "%s is not more in Junky Mode"%serie.name
            
    print "%s is on Junky Mode"%name
    

if __name__ == "__main__":
    args = parser.parse_args()
    if args.track:
        track(name = args.track)
    elif args.untrack:
        untrack(name = args.untrack)
    elif args.junky:
        junky(name = args.junky)
    

