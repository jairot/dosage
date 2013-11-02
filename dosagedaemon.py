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

from models import *
from tpb import TPB
from tpb import CATEGORIES, ORDERS


class TorrentClient(object):

    def __init__(self):
        self.client = transmissionrpc.Client()


class TorrentProvider(object):

    def __init__(self):
        self.provider = TPB('https://thepiratebay.sx') 

class DosageDaemon(object):
    
    def __init__(self):
        self.client = TorrentClient()
        self.provider = TorrentProvider()
        self.MINIMUM_SEEDS = 5
        pass

    def run(self):
        pass

if __name__ == "__main__":
    dosage = DosageDaemon()
    dosage.run()
