import unittest

from tvdosage.tvdosage import track, untrack, junky, delete, Series, startdb
from tvdosage.tvdosage import lister

class DosageBasicTest(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            pass

        def setUp(self):
            startdb(env='testing')

        def test_tracking(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name == "mad men")

            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a series
            track("Mad Men", 1, 0)

            series = Series.get(Series.name == "mad men")

            self.assertEqual(series.name, "mad men")
            self.assertEqual(series.last_season, 1)
            self.assertEqual(series.last_chapter, 0)
            self.assertTrue(series.tracking)

        def test_untracking(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name == "mad men")
            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a series
            track("Mad Men", 1, 0)

            series = Series.get(Series.name == "mad men")

            self.assertEqual(series.name, "mad men")
            self.assertEqual(series.last_season, 1)
            self.assertEqual(series.last_chapter, 0)
            self.assertTrue(series.tracking)

            #Stop tracking a Series
            untrack("Mad Men")

            series = Series.get(Series.name == "mad men")
            self.assertFalse(series.tracking)

        def test_junky_old(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name == "mad men")

            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a series
            track("Mad Men", 1, 0)
            series = Series.get(Series.name == "mad men")

            self.assertEqual(series.name, "mad men")
            self.assertEqual(series.last_season, 1)
            self.assertEqual(series.last_chapter, 0)
            self.assertTrue(series.tracking)
            self.assertFalse(series.junky)

            #Put that serie in Junky mode
            junky("Mad Men", 2, 3)
            series = Series.get(Series.name == "mad men")

            self.assertTrue(series.tracking)
            self.assertEqual(series.last_season, 2)
            self.assertEqual(series.last_chapter, 3)
            self.assertTrue(series.junky)

        def test_junky_new(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name == "mad men")

            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a serie in Junky mode
            junky("Mad Men", 2, 3)
            series = Series.get(Series.name == "mad men")

            self.assertEqual(series.name, "mad men")
            self.assertTrue(series.tracking)
            self.assertEqual(series.last_season, 2)
            self.assertEqual(series.last_chapter, 3)
            self.assertTrue(series.junky)

        def test_delete(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name == "mad men")

            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a series
            track("Mad Men", 1, 0)
            series = Series.get(Series.name == "mad men")

            self.assertEqual(series.name, "mad men")
            self.assertEqual(series.last_season, 1)
            self.assertEqual(series.last_chapter, 0)
            self.assertTrue(series.tracking)

            #Delete Serie from db
            delete("Mad Men")
            series = Series.select().where(Series.name == "mad men")

            self.assertRaises(IndexError, series.__getitem__, 0)

        def test_lists(self):
            lister()



if __name__ == '__main__':
    unittest.main()
