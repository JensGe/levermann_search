import datetime
import unittest
from utils import date_op as date


class TestDate(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_todays_date(self):
        calc_date = date.get_current_date().strftime("%d.%m.%Y")
        self.assertEqual(len(calc_date), 10)


    def test_get_date_one_year_ago(self):
        current_date = date.subtract_one_year(datetime.datetime(2018, 5, 1, 0, 0)).strftime("%d.%m.%Y")
        asserted_date = "01.05.2017"
        self.assertEqual(current_date, asserted_date)


    def test_get_last_days_of_month(self):
        asserted_last_months = [date.string_to_date('30.11.2018'),
                                date.string_to_date('31.10.2018'),
                                date.string_to_date('30.09.2018'),
                                date.string_to_date('31.08.2018')]
        last_months = date.get_last_days_of_last_four_months()
        self.assertEqual(asserted_last_months, last_months)


    def test_get_year_and_week_string(self):
        test_date_string = '22.12.2018'
        test_date = date.string_to_datetime(test_date_string)
        asserted_string = '2018-51'
        self.assertEqual(asserted_string, date.get_year_and_week_string(test_date))


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()