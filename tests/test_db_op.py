import unittest
from utils import date_op as date
from utils import db_op as db
from Parser import db_refresher


class TestDatabase(unittest.TestCase):

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

    def test_get_index_names(self):
        index_list = db.get_index_names()
        asserted_list = ['CAC_40', 'dax', 'dow_jones', 'Euro_Stoxx_50', 'FTSE_100', 'SMI']
        self.assertEqual(asserted_list, index_list)

    def test_get_pages_count(self):
        pages_1 = db.get_pages_count('FTSE_100')
        pages_2 = db.get_pages_count('SMI')
        asserted_pages_1 = 3
        asserted_pages_2 = 1
        self.assertEqual(asserted_pages_1, pages_1)
        self.assertEqual(asserted_pages_2, pages_2)

    def test_create_index_content_url_list(self):
        url_list = db.create_index_content_url_list()
        asserted_url_list = ['https://www.boerse-online.de/index/liste/CAC_40',
                             'https://www.boerse-online.de/index/liste/dax',
                             'https://www.boerse-online.de/index/liste/dow_jones',
                             'https://www.boerse-online.de/index/liste/Euro_Stoxx_50',
                             'https://www.boerse-online.de/index/liste/FTSE_100',
                             'https://www.boerse-online.de/index/liste/SMI']
        self.assertEqual(asserted_url_list, url_list)

    def test_check_if_exists(self):
        search = '010101'
        table = 'Aktien'
        column = 'ISIN'
        self.assertEqual(True, db.check_if_exists(search, table, column))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()