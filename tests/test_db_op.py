import unittest
from utils import date_op as date
from utils import db_op as db
from utils import constants as CST


class TestDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_all_index_names(self):
        index_list = db.get_all_index_names()
        asserted_list = ['CAC_40', 'dax', 'dow_jones', 'Euro_Stoxx_50', 'FTSE_100', 'SMI']
        self.assertEqual(asserted_list, index_list)

    def test_get_active_index_names(self):
        index_list = db.get_active_index_names()
        asserted_list = ['CAC_40', 'dax', 'dow_jones', 'Euro_Stoxx_50', 'FTSE_100',
                         'mdax', 'nasdaq_100', 's&p_500', 'sdax', 'SMI', 'tecdax']
        self.assertEqual(asserted_list, index_list)

    def test_get_pages_count(self):
        pages_1 = db.get_pages_count('FTSE_100')
        pages_2 = db.get_pages_count('SMI')
        asserted_pages_1 = 3
        asserted_pages_2 = 1
        self.assertEqual(asserted_pages_1, pages_1)
        self.assertEqual(asserted_pages_2, pages_2)

    def test_create_index_content_url_list(self):
        url_list = db.create_all_index_url_list(CST.URL_INDEX_CONTENT)
        asserted_url_list = ['https://www.boerse-online.de/index/liste/CAC_40',
                             'https://www.boerse-online.de/index/liste/dax',
                             'https://www.boerse-online.de/index/liste/dow_jones',
                             'https://www.boerse-online.de/index/liste/Euro_Stoxx_50',
                             'https://www.boerse-online.de/index/liste/FTSE_100',
                             'https://www.boerse-online.de/index/liste/SMI']
        self.assertEqual(asserted_url_list, url_list[:6])

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
        is_small_cap = db.is_small_cap('ab_inbev-Aktie')
        self.assertFalse(is_small_cap)

        is_small_cap_2 = db.is_small_cap('just_eat-Aktie')
        self.assertFalse(is_small_cap_2)

        is_small_cap_3 = db.is_small_cap('bechtle-Aktie')
        self.assertTrue(is_small_cap_3)

    def test_get_closing_stock_price(self):
        stock_uri = 'credit_suisse-Aktie'
        quarterly = '2018-11-01'
        closing_price, actual_date = db.get_closing_stock_price(quarterly, stock_uri)
        self.assertEqual(11.36, float(closing_price))

        quarterly_we = '2018-10-28'
        closing_price, actual_date = db.get_closing_stock_price(quarterly_we, stock_uri)
        self.assertEqual(10.92, float(closing_price))
        self.assertEqual('26.10.2018', date.date_to_string(actual_date))

    def test_get_latest_date_from_history(self):
        index_uri = 'dax'
        latest_date = db.get_latest_date_from_index_history(index_uri)
        asserted_date = date.string_to_date('29.10.2018')
        self.assertEqual(asserted_date, latest_date)

    def test_get_index_of_stock(self):
        stock_uri = 'credit_suisse-Aktie'
        index_uri = db.get_index_of_stock(stock_uri)
        self.assertEqual('SMI', index_uri)

    def test_get_indizes_of_stock(self):
        stock_uri = 'adidas-Aktie'
        index_list = db.get_indizes_of_stock(stock_uri)
        asserted_index_list = sorted(['dax', 'Euro_Stoxx_50'])
        self.assertEqual(asserted_index_list, index_list)

    def test_get_stock_names(self):
        asserted_stock_list = ['aktie1', 'aktie2', 'aktie3']
        stock_names = db.get_stock_names()
        self.assertEqual(asserted_stock_list, stock_names[:3])

    def test_get_stock_names_and_history_url(self):
        stock_and_history_url_list = db.get_stock_names_and_history_url()
        asserted_list = [['21st_century_fox_a-Aktie', 'FSE'],
                         ['21st_century_fox_b-Aktie', 'FSE'],
                         ['3i-Aktie', 'FSE']]
        print(stock_and_history_url_list)
        self.assertEqual(asserted_list, stock_and_history_url_list[:3])

    def test_get_stock_history_url_list(self):
        stock_history_list = [['aktie1-Aktie', 'FSE'],
                              ['aktie2-Aktie', 'XETRA'],
                              ['aktie3-Aktie', 'FSE']]
        base_url = 'https://www.boerse-online.de/kurse/historisch/'
        url_list = [base_url + stock[0] + '/' + stock[1] for stock in stock_history_list]
        asserted_url_list = ['https://www.boerse-online.de/kurse/historisch/aktie1/FSE',
                             'https://www.boerse-online.de/kurse/historisch/aktie2/XETRA',
                             'https://www.boerse-online.de/kurse/historisch/aktie3/FSE']
        self.assertEqual(asserted_url_list, url_list)

    def test_calculate_list_change(self):
        input_list = [100, 90, 99, 49.5]
        asserted_list = [-0.1, 0.1, -0.5]
        self.assertEqual(asserted_list, db.calculate_list_changes(input_list))

    def test_check_financial_companies(self):
        stock_uri = '3i-Aktie'
        self.assertTrue(db.check_is_financial_company(stock_uri))

        stock_uri_2 = 'abbvie-Aktie'
        self.assertFalse(db.check_is_financial_company(stock_uri_2))

        stock_uri_3 = 'affiliated_managers_group-Aktie'
        self.assertTrue(db.check_is_financial_company(stock_uri_3))

        stock_uri_4 = 'amazon-Aktie'
        self.assertFalse(db.check_is_financial_company(stock_uri_4))

        stock_uri_5 = 'bbva-Aktie'
        self.assertTrue(db.check_is_financial_company(stock_uri_5))

    def test_write_list_to_db(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
