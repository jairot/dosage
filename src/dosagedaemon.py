#!/urs/bin/env python
#-*- coding: utf-8 -*-
""" This daemon downloads and schedules the Series that dosage is tracking
because Bandwith is allways scarce there are some policies implemented in
order to improve the performance and make the dosage daemon the less invasive
posible.

The policies for downloading Tv Series are:

1) Never download More than one chapter per TV Series.

2) Allways download chapters with the max number of seeds.

3) Never download chapters with less than 5 seeds.

3) Only one Tv Series Can be at Junky mode at the time.

4) If 1 Tv Series is in Junky mode, don't download new chapters of tracking
   series

5) When you download the last chapter of a Tv Series on Junky mode, the junky
mode stops.

"""

import transmissionrpc
import mattdaemon
import sys
import logging
import sqlite3

from time import sleep
from models import *
from tpb import TPB
from tpb import ORDERS


logging.basicConfig()


class TorrentClient(object):

    def __init__(self):
        #Let's assume that Trasmission is On and fix It later
        #TODO: What happens when transsmission is not on?
        self.client = transmissionrpc.Client()

    def already_downloading(self, name):
        """Checks if at least one chapter is Downloading"""
        #Common torrent nomenclature replaces the space with a dot.
        name = name.replace(" ", ".")
        altname = name.replace(".", "+")
        for torrent in self.client.get_torrents():
            if name in torrent.name.lower() or altname in torrent.name.lower():
                if torrent.progress != 100:
                    return True
        return False

    def download(self, magnet):
        try:
            self.client.add_torrent(magnet)
        except transmissionrpc.error.TransmissionError:
            print "Already downloaded that torrent"


class TorrentProvider(object):

    def __init__(self):
        self.provider = TPB('https://thepiratebay.sx')

    def find(self, seriename):
        print "Searching for %s" % seriename
        search = self.provider.search(seriename)
        search.order(ORDERS.SEEDERS.ASC).multipage()
        try:
            torrent = next(search.items())
        except StopIteration:
            return None
        else:
            return torrent.magnet_link


class DosageDaemon(object):

    def __init__(self, client=TorrentClient, provider=TorrentProvider):
        self.client = client()
        self.provider = provider()
        self.MINIMUM_SEEDS = 5

    def download(self, serie):
        #TODO: Crapy logic, make it better
        seriename, chapter, season = self.stringmaker(serie)
        torrent = self.provider.find(seriename)

        #Lookup if a new season is available
        if not torrent:
            seriename, chapter, season = self.stringmaker(serie, newseason=1)
            torrent = self.provider.find(seriename)

        if torrent:
            self.client.download(torrent)
            serie.last_chapter = chapter
            serie.last_season = season
            serie.save()

    def stringmaker(self, serie, newseason=0):
        if newseason == 1:
            chapter = str(1).zfill(2)
        else:
            chapter = str(serie.last_chapter + 1).zfill(2)
        season = str(serie.last_season + newseason).zfill(2)
        seriestring = serie.name + ' S' + season + 'E' + chapter
        return seriestring, chapter, season

    def run(self):
        serie = self.get_junky()
        if serie:
            serie = serie[0]  # Just One Junkie at the time Remember!
            if not self.client.already_downloading(serie.name):
                self.download(serie)
        else:
            series = self.get_tracking()
            for serie in series:
                if not self.client.already_downloading(serie.name):
                    self.download(serie)

    def get_junky(self):
        series = Series.select().where(Series.junkie == True)
        try:
            series[0]
        except IndexError:
            series = []
        return series

    def get_tracking(self):
        series = Series.select().where(Series.tracking == True)
        return series

    def already_downloading(self):
        pass


class MyDaemon(mattdaemon.daemon):

    def run(self, *args, **kwargs):
        dosage = DosageDaemon()
        while True:
            startdb()
            try:
                dosage.run()
            except sqlite3.InterfaceError:
                print "Sqlite Interface Error"
            closedb()
            sleep(10)


if __name__ == "__main__":

    args = {
           "pidfile": "/tmp/dosage-daemon.pid",
           "stdout": "/tmp/dosage-daemon.log",
           "stderr": "/tmp/dosage-daemon.log",
           "daemonize": True
           }
    daem = MyDaemon(**args)

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ("-h", "--help"):
            print("python " + sys.argv[0] + " start|stop|restart|status|logs")
        elif arg in ("start", "start-no-daemon"):
            daem.start()
        elif arg in ("stop"):
            daem.stop()
        elif arg in ("restart"):
            daem.restart()
        elif arg in ("status"):
            if daem.status():
                print("dosage daemon currently running! :)")
            else:
                print("dosage daemon not running! :(")
                print("Check out the log in %s" % args["stderr"])
        elif arg in ("logs"):
            f = open(args['stderr'])
            log = f.readlines(size=100)
            print(log)
        else:
            print "Unknown arg:", arg
