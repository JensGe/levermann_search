import unittest
from utils import date_op as date
from utils import db_op as db
from Scrapper import db_refresher


class TestDate(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_closingprice_from_date(self):
        query_date = date.string_to_date("07.09.2018")
        calc_price = db.get_closing_price_from_date(query_date, 'dax')
        asserted_price = '11.959,63'
        self.assertEqual(asserted_price, calc_price)

    def test_get_intervall(self):
        start, end = db_refresher.select_index_intervall("dax")
        asserted_start = "06.10.2018"
        self.assertEqual(start, asserted_start)

    def test_get_max_date(self):
        max_date = db.get_max_date_of_index_history("dax")
        asserted_max_date = "05.10.2018"
        self.assertEqual(max_date, asserted_max_date)


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()