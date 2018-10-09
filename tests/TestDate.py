import datetime
import unittest
from utils import date_op as date


class TestDate(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_todays_date(self):
        calc_date = date.get_todays_date().strftime("%d.%m.%Y")
        self.assertEqual(len(calc_date), 10)

    def test_get_date_six_months_ago(self):
        current_date = date.subtract_six_months(datetime.datetime(2018, 5, 1, 0, 0)).strftime("%d.%m.%Y")
        asserted_date = "01.11.2017"
        self.assertEqual(current_date, asserted_date)

    def test_get_date_one_year_ago(self):
        current_date = date.subtract_one_year(datetime.datetime(2018, 5, 1, 0, 0)).strftime("%d.%m.%Y")
        asserted_date = "01.05.2017"
        self.assertEqual(current_date, asserted_date)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()