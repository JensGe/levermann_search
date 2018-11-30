import unittest
from utils import date_op as date
from utils import db_op as db
from Parser import db_refresher
from utils import constants as CST


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
        url_list = db.create_index_url_list(CST.URL_INDEX_CONTENT)
        asserted_url_list = ['https://www.boerse-online.de/index/liste/CAC_40',
                             'https://www.boerse-online.de/index/liste/dax',
                             'https://www.boerse-online.de/index/liste/dow_jones',
                             'https://www.boerse-online.de/index/liste/Euro_Stoxx_50',
                             'https://www.boerse-online.de/index/liste/FTSE_100',
                             'https://www.boerse-online.de/index/liste/SMI']
        self.assertEqual(asserted_url_list, url_list[:6])


    # DB Tests
    ####################
    # def test_check_if_exists(self):
    #     search = '010101'
    #     table = 'Aktien'
    #     column = 'ISIN'
    #     self.assertEqual(True, db.check_if_exists(search, table, column))
    #
    # def test_write_stock_to_stock_table(self):
    #     stock = ['Test1', 'XX00X0XX000', 'Test-Aktie']
    #     db.write_stock_to_stock_table(stock)
    #
    # def test_write_stock_to_stock_content_table(self):
    #     stock = 'XX00X0XX000'
    #     index_name = 'dax'
    #     current_date = date.get_todays_date()
    #     db.write_stock_to_stock_contents_table(stock, index_name, current_date)
    #
    # def test_write_stock_history_to_db(self):
    #     index_URI = 'CAC_40'
    #     index_history = [['01.10.2018', 9127.05, 9094.28],
    #                      ['02.10.2018', 9087.32, 9076.57],
    #                      ['03.10.2018', 9175.21, 9126.31]]
    #     db.write_stock_history_to_db(index_history, index_URI)

    def test_get_earnings_after_tax(self):
        result = db.get_earnings_after_tax('ab_inbev-Aktie')
        self.assertEqual(7089.06, result)

    def test_get_equity_capital(self):
        result = db.get_equity_capital('ab_inbev-Aktie')
        self.assertEqual(66805.46, result)

    def test_eps_s(self):
        eps_s = db.get_eps('ab_inbev-Aktie')
        self.assertEqual([4.55, 0.65, 3.60, 3.47, 4.22], eps_s)

    def test_ratings(self):
        ratings = db.get_analyst_ratings('ab_inbev-Aktie')
        self.assertEqual([1, 0, 0], ratings)

    def test_caps(self):
        is_cap = db.is_small_cap('ab_inbev-Aktie')
        self.assertFalse(is_cap)

    def test_get_closing_stock_price(self):
        stock_uri = 'credit_suisse-Aktie'
        quarterly = '2018-11-01'
        closing_price = db.get_closing_stock_price(quarterly, stock_uri)
        self.assertEqual(11.36, float(closing_price))

        quarterly_we = '2018-10-28'
        closing_price = db.get_closing_stock_price(quarterly_we, stock_uri)
        self.assertEqual(10.92, float(closing_price))

    def test_get_latest_date_from_history(self):
        index_uri = 'dax'
        latest_date = db.get_latest_date_from_index_history(index_uri)
        asserted_date = date.string_to_date('29.10.2018')
        self.assertEqual(asserted_date, latest_date)



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()