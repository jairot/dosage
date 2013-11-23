import unittest

from mock import Mock, call
from models import Series, startdb
from dosagedaemon import DosageDaemon, TorrentClient, TorrentProvider
from tvdosage import track, untrack, junky


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

        def test_already_downloading(self):
            track("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = True
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.assertFalse(self.daemon.provider.find.called)

        def test_junky(self):
            junky("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S02E02")
            self.daemon.client.download.assert_called_once_with("MadMenMagnet")

        def test_junky_vs_track(self):
            track("The Wire", 1, 0)
            junky("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S02E02")
            self.daemon.client.download.assert_called_once_with("MadMenMagnet")

        def test_stringmaker(self):
            track("The Wire", 1, 0)

            serie = Series.get(Series.name=="the wire")

            seriestring = self.daemon.stringmaker(serie)
            self.assertEqual(seriestring, ('the wire S01E01', '01', '01'))

            seriestring = self.daemon.stringmaker(serie, newseason=1)
            self.assertEqual(seriestring, (u'the wire S02E01', '01', '02'))

        def test_cant_find_magnet(self):
            track("Mad Men", 1, 0)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = None

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")

            calls = [call("mad men S01E01"), call("mad men S02E01")]

            self.daemon.provider.find.assert_has_calls(calls)
            self.assertFalse(self.daemon.client.download.called)

