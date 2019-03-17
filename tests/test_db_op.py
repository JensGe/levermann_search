import unittest
from utils import date_op as date
from utils import db_op as db
from utils import constants as cst
from tests import db_test as db_test


class TestDatabase(unittest.TestCase):
    def setUp(self):
        db_test.create_test_tables()
        db_test.insert_test_data()

    # get_list()
    def test_get_list_from_db(self):
        index_list = db.get_list(
            table=cst.TABLE_INDIZES, columns=cst.COLUMN_URI, database=cst.TEST_DATABASE
        )
        asserted_list = ["CAC_40", "dax", "dow_jones", "FTSE_100", "s&p_500", "tecdax"]
        self.assertEqual(asserted_list, index_list)

    def test_get_list_from_db_with_condition(self):
        index_list = db.get_list(
            table=cst.TABLE_INDIZES,
            columns=cst.COLUMN_URI,
            condition=[cst.COLUMN_LARGECAP, b"1"],
            database=cst.TEST_DATABASE,
        )
        asserted_list = ["CAC_40", "dax", "dow_jones", "FTSE_100"]
        self.assertEqual(asserted_list, index_list)

    def test_get_two_column_list_from_db(self):
        stock_list = db.get_list(
            table=cst.TABLE_STOCKS,
            columns=[cst.COLUMN_URI, cst.COLUMN_MARKET_PLACE],
            database=cst.TEST_DATABASE,
        )
        asserted_list = [
            ["3i-Aktie", "FSE"],
            ["3m-Aktie", "FSE"],
            ["ab_inbev-Aktie", "FSE"],
            ["adidas-Aktie", "FSE"],
            ["bechtle-Aktie", "FSE"],
            ["cellcom_israel-Aktie", "FSE"],
            ["coca-cola-Aktie", "FSE"],
        ]
        self.assertEqual(asserted_list, stock_list)

    # get_item()
    def test_get_latest_date_from_index_history_with_condition(self):
        asserted_latest_date = date.string_to_date("08.03.2019")
        actual_latest_date = db.get_item(
            table=cst.TABLE_INDEX_HISTORIES,
            column="max(Datum)",
            condition=[cst.COLUMN_INDEX_URI, "dax"],
            database=cst.TEST_DATABASE,
        )
        self.assertEqual(asserted_latest_date, actual_latest_date)

    def test_get_latest_date_from_index_history_which_does_not_exist(self):
        actual_latest_date = db.get_item(
            table=cst.TABLE_INDEX_HISTORIES,
            column="max(Datum)",
            condition=[cst.COLUMN_INDEX_URI, "bux"],
            database=cst.TEST_DATABASE,
        )
        self.assertIsNone(actual_latest_date)

    def test_get_latest_date_from_stock_history_with_condition(self):
        asserted_latest_date = date.string_to_date("01.02.2019")
        actual_latest_date = db.get_item(
            table=cst.TABLE_STOCKS_HISTORIES,
            column="max(Datum)",
            condition=[cst.COLUMN_STOCK_URI, "Adidas-Aktie"],
            database=cst.TEST_DATABASE,
        )
        self.assertEqual(asserted_latest_date, actual_latest_date)

    # Todo write
    def test_write_stock_overview_history_to_db(self):
        overview_stock_history = [
            ["08.02.2019", "197,90"],
            ["07.02.2019", "197,90"],
            ["06.02.2019", "201,60"],
            ["05.02.2019", "202,70"],
            ["04.02.2019", "196,45"],
        ]
        stock_uri = "adidas-Aktie"
        self.assertTrue(
            db.write_stock_overview_history_to_db(
                overview_stock_history, stock_uri, cst.TEST_DATABASE
            )
        )

        asserted_database_content = [
            ["adidas-Aktie", date.string_to_date("28.01.2019"), 203.10, 202.80],
            ["adidas-Aktie", date.string_to_date("29.01.2019"), 203.20, 204.90],
            ["adidas-Aktie", date.string_to_date("30.01.2019"), 204.10, 205.90],
            ["adidas-Aktie", date.string_to_date("31.01.2019"), 206.90, 207.40],
            ["adidas-Aktie", date.string_to_date("01.02.2019"), 202.30, 199.40],
            ["adidas-Aktie", date.string_to_date("04.02.2019"), None, 196.45],
            ["adidas-Aktie", date.string_to_date("05.02.2019"), None, 202.70],
            ["adidas-Aktie", date.string_to_date("06.02.2019"), None, 201.60],
            ["adidas-Aktie", date.string_to_date("07.02.2019"), None, 197.90],
            ["adidas-Aktie", date.string_to_date("08.02.2019"), None, 197.90],
        ]
        validating_list = db.get_list(
            table=cst.TABLE_STOCKS_HISTORIES,
            columns=[
                cst.COLUMN_STOCK_URI,
                cst.COLUMN_DATE,
                cst.COLUMN_START_VALUE,
                cst.COLUMN_CLOSING_VALUE,
            ],
            condition=[cst.COLUMN_STOCK_URI, "adidas-Aktie"],
            database=cst.TEST_DATABASE,
        )
        converted_validating_list = [
            [
                item[0],
                item[1],
                float(item[2]) if item[2] is not None else None,
                float(item[3]) if item[3] is not None else None,
            ]
            for item in validating_list
        ]
        self.assertEqual(asserted_database_content, converted_validating_list)

    #
    # def test_write_stock_history_to_db_from_history_data(self):
    #     history_stock_data = [
    #         ['adidas-Aktie', '2019 - 02 - 07', '', ''],
    #         ['adidas-Aktie', '', '', ''],
    #         ['adidas-Aktie', '', '', ''],
    #         ['adidas-Aktie', '', '', ''],
    #         ['adidas-Aktie', '', '', ''],
    #     ]
    #
    #                 201.50    199.50
    #         adidas - Aktie    2019 - 02 - 06    202.80    201.60
    #         adidas - Aktie    2019 - 02 - 05    197.40    202.70
    #         adidas - Aktie    2019 - 02 - 04    199.45    196.45

    # uncategorized tests
    def test_convert_list_to_db_value_string(self):
        input_data_list = [
            ["adidas AG", "07.11.18", "Quartalszahlen", "Future"],
            ["adidas AG", "07.03.19", "Quartalszahlen", "Future"],
            ["adidas AG", "02.05.19", "Quartalszahlen", "Future"],
        ]
        asserted_list_string = (
            "('adidas AG', '07.11.18', 'Quartalszahlen', 'Future'), "
            "('adidas AG', '07.03.19', 'Quartalszahlen', 'Future'), "
            "('adidas AG', '02.05.19', 'Quartalszahlen', 'Future')"
        )
        self.assertEqual(
            asserted_list_string, db.convert_list_to_db_value_string(input_data_list)
        )

        input_data_list_2 = [["adidas AG", "07.11.18", "Quartalszahlen", "Future"]]
        asserted_list_string_2 = "('adidas AG', '07.11.18', 'Quartalszahlen', 'Future')"
        self.assertEqual(
            asserted_list_string_2,
            db.convert_list_to_db_value_string(input_data_list_2),
        )

    def test_insert_future_dates_table(self):
        rv = db.insert_list(
            table="Aktientermine",
            data=[
                ["adidas AG", "2018-11-07", "Quartalszahlen", "Future"],
                ["adidas AG", "2018-03-07", "Quartalszahlen", "Future"],
                ["adidas AG", "2019-05-02", "Quartalszahlen", "Future"],
            ],
            database=cst.TEST_DATABASE,
        )
        self.assertTrue(rv)

    def test_insert_past_dates_table(self):
        rv = db.insert_list(
            table="Aktientermine",
            data=[
                ["adidas AG", "2018-08-09", "Q2 2018 Earnings Release", "Past"],
                ["adidas AG", "2018-05-09", "Hauptversammlung", "Past"],
                ["adidas AG", "2017-11-09", "Q3 2017", "Past"],
            ],
            database=cst.TEST_DATABASE,
        )
        self.assertTrue(rv)

    def test_create_index_content_url_list(self):
        url_list = db.create_all_index_url_list(
            cst.URL_INDEX_CONTENT, database=cst.TEST_DATABASE
        )
        asserted_url_list = [
            "https://www.boerse-online.de/index/liste/CAC_40",
            "https://www.boerse-online.de/index/liste/dax",
            "https://www.boerse-online.de/index/liste/dow_jones",
            "https://www.boerse-online.de/index/liste/FTSE_100",
            "https://www.boerse-online.de/index/liste/s&p_500",
            "https://www.boerse-online.de/index/liste/tecdax",
        ]
        self.assertEqual(asserted_url_list, url_list[:6])

    #
    #
    # ToDo renew with Testdatabase

    def test_get_earnings_after_tax(self):
        result = db.get_earnings_after_tax("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual(3702.48, result)

    def test_get_equity_capital(self):
        result = db.get_equity_capital("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual(62899.88, result)

    def test_eps_s(self):
        eps_s = db.get_eps("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual([0.65, 3.60, 1.87, 4.11, 4.49], eps_s)

    def test_ratings(self):
        ratings = db.get_analyst_ratings("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual([6, 2, 0], ratings)

    def test_caps_large(self):
        is_small_cap = db.is_small_cap("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertFalse(is_small_cap)

    def test_caps_small(self):
        is_small_cap = db.is_small_cap("bechtle-Aktie", database=cst.TEST_DATABASE)
        self.assertTrue(is_small_cap)

    def test_get_closing_stock_price_weekday(self):
        stock_uri = "adidas-Aktie"
        quarterly = "2019-01-29"
        closing_price, actual_date = db.get_closing_stock_price(
            quarterly, stock_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(204.90, float(closing_price))

    def test_get_closing_stock_price_weekend(self):
        stock_uri = "adidas-Aktie"
        quarterly_we = "2019-02-03"
        closing_price, actual_date = db.get_closing_stock_price(
            quarterly_we, stock_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(199.40, float(closing_price))
        self.assertEqual("01.02.2019", date.date_to_string(actual_date))

    def test_get_main_index_of_stock(self):
        stock_uri = "3i-Aktie"
        index_uri = db.get_main_index_of_stock(stock_uri, database=cst.TEST_DATABASE)
        self.assertEqual("FTSE_100", index_uri)

    def test_get_indices_of_stock(self):
        stock_uri = "3m-Aktie"
        index_list = db.get_indices_of_stock(stock_uri, database=cst.TEST_DATABASE)
        asserted_index_list = sorted(["dow_jones", "s&p_500"])
        self.assertEqual(asserted_index_list, index_list)

    def test_get_stock_history_url_list(self):
        stock_history_list = [
            ["aktie1-Aktie", "FSE"],
            ["aktie2-Aktie", "XETRA"],
            ["aktie3-Aktie", "FSE"],
        ]
        base_url = "https://www.boerse-online.de/kurse/historisch/"
        url_list = [
            base_url + stock[0][:6] + "/" + stock[1] for stock in stock_history_list
        ]
        asserted_url_list = [
            "https://www.boerse-online.de/kurse/historisch/aktie1/FSE",
            "https://www.boerse-online.de/kurse/historisch/aktie2/XETRA",
            "https://www.boerse-online.de/kurse/historisch/aktie3/FSE",
        ]
        self.assertEqual(asserted_url_list, url_list)

    def test_calculate_list_change(self):
        input_list = [100, 90, 99, 49.5]
        asserted_list = [-0.1, 0.1, -0.5]
        self.assertEqual(asserted_list, db.calculate_list_changes(input_list))

    def test_check_financial_companies_true(self):
        stock_uri = "3i-Aktie"
        self.assertTrue(
            db.check_is_financial_company(stock_uri, database=cst.TEST_DATABASE)
        )

    def test_check_financial_companies_false(self):
        stock_uri = "bechtle-Aktie"
        self.assertFalse(
            db.check_is_financial_company(stock_uri, database=cst.TEST_DATABASE)
        )

    def test_write_list_to_db(self):
        # Todo
        pass

    def tearDown(self):
        db_test.delete_test_data()
        db_test.drop_test_tables()
        pass


if __name__ == "__main__":
    unittest.main()
