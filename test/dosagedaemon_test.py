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
            self.tpmock = Mock(spec=TorrentProvider)
            self.tcmock = Mock(spec=TorrentClient)
            self.daemon = DosageDaemon(self.tcmock, self.tpmock)

        def test_empty_db(self):
            self.daemon.run()

        def test_new_serie(self):
            track("Mad Men", 1, 0)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S01E01")
            self.daemon.client.downdloadassert_called_once_with("MadMenMagnet")
