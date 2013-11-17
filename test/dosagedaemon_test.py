import unittest

from mock import Mock
from models import Series, startdb
from dosagedaemon import DosageDaemon, TorrentClient, TorrentProvider
from dosage import track, untrack, junky, delete



class DosageDaemonTest(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            pass

        def setUp(self):
            startdb(env='testing')
            tpmock = Mock(spec=TorrentProvider)
            tcmock = Mock(spec=TorrentClient)
            daemon = DosageDaemon(tcmock, tpmock)

