#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""This Module works as a Dosage Runner"""

import argparse
import logmanager as log

from models import *


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--track", help="Start tracking the given tv series")
parser.add_argument("-u", "--untrack",
                    help="Stop tracking the given tv series")
parser.add_argument("-j", "--junky",
                    help="Put the given tv series on Junky mode")
parser.add_argument("-d", "--delete", help="Deletes a TV Series from the DB")
parser.add_argument("-s,", "--season", help="Declares a season Offset",
                    type=int, default=1)
parser.add_argument("-c,", "--chapter", help="Declares a Chapter Offset",
                    type=int, default=1)
parser.add_argument("-l,", "--list", help="list all the seriesi in the DB",
                    action="store_true")


def track(name, season, chapter):
    name = name.lower()
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        serie = Series.create(name=name, last_season=season,
                              last_chapter=chapter, tracking=True)
    else:
        serie.tracking = True
        serie.save()
    print "Tracking %s" % name


def untrack(name):
    name = name.lower()
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        print "You are not Tracking that Tv Series"
    else:
        serie.tracking = False
        serie.junky = False
        serie.save()
        print "Untracking %s" % name


def junky(name, season, chapter):
    name = name.lower()
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        serie = Series.create(name=name, last_season=season,
                              last_chapter=chapter, tracking=True, junky=True)
    else:
        serie.tracking = True
        serie.junky = True
        if serie.last_season <= season:
            serie.last_season = season
            if serie.last_chapter < chapter:
                serie.last_chapter = chapter
        serie.save()
    finally:
        #No more than 1 tv series in junky mode at the time
        series = Series.select().where(Series.name != name,
                                       Series.junky == True)
        for serie in series:
            serie.junky = False
            serie.save()
            print "%s is not more in Junky Mode" % serie.name
    print "%s is on Junky Mode" % name


def delete(name):
    name = name.lower()
    try:
        serie = Series.get(Series.name == name)
    except Series.DoesNotExist:
        print "There is not serie with that name on the DB"
    else:
        serie.delete_instance()
        print "%s has been removed from the DB" % name


def lister():
    series = Series.select()
    for serie in series:
        if serie.tracking:
            print "Tracking %s in Chapter %s and season %s" % \
                  (serie.name, str(serie.last_chapter),
                   str(serie.last_season))
        else:
            print "Not Tracking %s since Chapter %s and season %s" % \
                  (serie.name, str(serie.last_chapter),
                   str(serie.last_season))

def main():
    args = parser.parse_args()
    startdb()
    if args.track:
        track(name=args.track, chapter=args.chapter - 1,
              season=args.season)
    elif args.untrack:
        untrack(name=args.untrack)
    elif args.junky:
        junky(name=args.junky, chapter=args.chapter - 1,
              season=args.season)
    elif args.list:
        lister()
    elif args.delete:
        delete(name=args.delete)

if __name__ == "__main__":
    main()
