import unittest

from models import Series, startdb
from dosage import track

class DosageBasicTest(unittest.TestCase):

        def setUp(self):
            startdb(env='testing')

        def test_tracking(self):
            #Check if mad men is not in Series
            series = Series.select().where(Series.name=="Mad Men")

            self.assertRaises(IndexError, series.__getitem__, 0)

            #Start tracking a series
            track("Mad Men", 1, 0)

            series = Series.get(Series.name=="mad men")

            self.assertEqual(series.name, "mad men")
            self.assertEqual(series.last_season, 1)
            self.assertEqual(series.last_chapter, 0)


if __name__ == '__main__':
    unittest.main()
