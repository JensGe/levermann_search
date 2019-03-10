import unittest
from utils import date_op as date
from utils import db_op as db
from utils import constants as CST


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """
        create table Aktien (
            ISIN varchar(127),
            WKN varchar(127),
            Name varchar(255) not null,
            Waehrung varchar(5),
            URI varchar(255) primary key,
            Handelsplatz varchar(15));

        ...
        """

    def test_db_select(self):
        index_list = db.get_list(table=CST.TABLE_INDIZES, columns=CST.COLUMN_URI, test=True)
        asserted_list = ['dax', 'CAC_40', 'dow_jones']
        self.assertEqual(asserted_list, index_list)

        index_list_2 = db.get_list(table=CST.TABLE_INDIZES, columns=CST.COLUMN_URI,
                                   condition=[CST.COLUMN_ACTIVE, 1], test=True)
        asserted_list_2 = ['dax', 'CAC_40']
        self.assertEqual(asserted_list_2, index_list_2)

        stock_list_3 = db.get_list(table=CST.TABLE_STOCKS, columns=[CST.COLUMN_URI, CST.COLUMN_MARKET_PLACE], test=True)
        asserted_list_3 = [['adidas-Aktie', 'FSE'], ['coca-cola-Aktie', 'FSE']]
        self.assertEqual(asserted_list_3, stock_list_3)

        stock_list_4 = db.get_list(table=CST.TABLE_STOCKS, columns=CST.COLUMN_URI, test=True)
        asserted_list_4 = ['adidas-Aktie', 'coca-cola-Aktie']
        self.assertEqual(asserted_list_4, stock_list_4)

    def test_create_index_content_url_list(self):
        url_list = db.create_all_index_url_list(CST.URL_INDEX_CONTENT)
        asserted_url_list = ['https://www.boerse-online.de/index/liste/CAC_40',
                             'https://www.boerse-online.de/index/liste/dax',
                             'https://www.boerse-online.de/index/liste/dow_jones',
                             'https://www.boerse-online.de/index/liste/Euro_Stoxx_50',
                             'https://www.boerse-online.de/index/liste/FTSE_100',
                             'https://www.boerse-online.de/index/liste/SMI']
        self.assertEqual(asserted_url_list, url_list[:6])

    def test_get_latest_date_from_index_history(self):
        asserted_latest_date = '2019-01-25'
        actual_latest_date = db.get_item(table=CST.TABLE_INDEX_HISTORIES, column='max(Datum)',
                                         condition=[CST.COLUMN_INDEX_URI, 'dax'], test=True)
        self.assertEqual(asserted_latest_date, actual_latest_date)

        actual_latest_date_2 = db.get_item(table=CST.TABLE_INDEX_HISTORIES, column='max(Datum)',
                                           condition=[CST.COLUMN_INDEX_URI, 'dow_jones'], test=True)
        self.assertIsNone(actual_latest_date_2)

        actual_latest_date_3 = db.get_item(table=CST.TABLE_STOCKS_HISTORIES, column='max(Datum)',
                                           condition=[CST.COLUMN_STOCK_URI, 'Adidas-Aktie'], test=True)
        self.assertTrue(actual_latest_date_3)

#
#
# ToDo renew with Testdatabase

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

    def test_get_index_of_stock(self):
        stock_uri = 'credit_suisse-Aktie'
        index_uri = db.get_index_of_stock(stock_uri)
        self.assertEqual('SMI', index_uri)

    def test_get_indizes_of_stock(self):
        stock_uri = 'adidas-Aktie'
        index_list = db.get_indizes_of_stock(stock_uri)
        asserted_index_list = sorted(['dax', 'Euro_Stoxx_50'])
        self.assertEqual(asserted_index_list, index_list)

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
