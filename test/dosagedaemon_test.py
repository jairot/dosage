import unittest

from mock import Mock, call
from dosagedaemon import DosageDaemon, TorrentClient, TorrentProvider
from dosagedaemon import Series, startdb


def faketrack(name, season, chapter):
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

def fakejunky(name, season, chapter):
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
            faketrack("Mad Men", 1, 0)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S01E01")
            self.daemon.client.downdloadassert_called_once_with("MadMenMagnet")

        def test_already_downloading(self):
            faketrack("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = True
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.assertFalse(self.daemon.provider.find.called)

        def test_junky(self):
            fakejunky("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S02E02")
            self.daemon.client.download.assert_called_once_with("MadMenMagnet")

        def test_junky_vs_track(self):
            faketrack("The Wire", 1, 0)
            fakejunky("Mad Men", 2, 1)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = "MadMenMagnet"

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")
            self.daemon.provider.find.assert_called_once_with("mad men S02E02")
            self.daemon.client.download.assert_called_once_with("MadMenMagnet")

        def test_stringmaker(self):
            faketrack("The Wire", 1, 0)

            serie = Series.get(Series.name=="the wire")

            seriestring = self.daemon.stringmaker(serie)
            self.assertEqual(seriestring, ('the wire S01E01', '01', '01'))

            seriestring = self.daemon.stringmaker(serie, newseason=1)
            self.assertEqual(seriestring, (u'the wire S02E01', '01', '02'))

        def test_cant_find_magnet(self):
            faketrack("Mad Men", 1, 0)

            self.daemon.client.already_downloading.return_value = False
            self.daemon.provider.find.return_value = None

            self.daemon.run()

            self.daemon.client.already_downloading.\
                        assert_called_once_with("mad men")

            calls = [call("mad men S01E01"), call("mad men S02E01")]

            self.daemon.provider.find.assert_has_calls(calls)
            self.assertFalse(self.daemon.client.download.called)

