import unittest
from utils import date_op as date
from utils import db_op as db
from utils import constants as cst
from tests import db_test as db_test


class TestDatabase(unittest.TestCase):
    def setUp(self):
        db_test.delete_test_data()
        db_test.drop_test_tables()
        db_test.create_test_tables()
        db_test.insert_test_data()
        pass

    # get_list()
    def test_get_list_from_db(self):
        index_list = db.get_list(
            table=cst.TABLE_INDIZES, columns=cst.COLUMN_URI, database=cst.TEST_DATABASE
        )
        asserted_list = ["CAC_40", "dax", "dow_jones", "FTSE_100", "s&p_500", "tecdax"]
        self.assertEqual(asserted_list.sort(), index_list.sort())
        # self.assertEqual(asserted_list, index_list)

    def test_get_list_from_db_with_condition(self):
        index_list = db.get_list(
            table=cst.TABLE_INDIZES,
            columns=cst.COLUMN_URI,
            condition=[cst.COLUMN_LARGECAP, 1],
            database=cst.TEST_DATABASE,
        )
        asserted_list = ["CAC_40", "dax", "dow_jones", "FTSE_100"]
        self.assertEqual(asserted_list.sort(), index_list.sort())

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
        self.assertEqual(asserted_list.sort(), stock_list.sort())

    # get_list Calculations
    def test_create_active_index_url_list_from_index_content_url(self):
        asserted_index_list = [
            "https://www.boerse-online.de/index/liste/CAC_40",
            "https://www.boerse-online.de/index/liste/dax",
            "https://www.boerse-online.de/index/liste/dow_jones",
            "https://www.boerse-online.de/index/liste/FTSE_100",
            "https://www.boerse-online.de/index/liste/s&p_500",
            "https://www.boerse-online.de/index/liste/tecdax",
        ]
        calculated_index_list = db.create_active_index_url_list(
            cst.URL_INDEX_CONTENT, cst.TEST_DATABASE
        )
        self.assertEqual(asserted_index_list.sort(), calculated_index_list.sort())

    def test_create_active_index_url_list_from_index_history_url(self):
        asserted_index_list = [
            "https://www.boerse-online.de/index/historisch/CAC_40",
            "https://www.boerse-online.de/index/historisch/dax",
            "https://www.boerse-online.de/index/historisch/dow_jones",
            "https://www.boerse-online.de/index/historisch/FTSE_100",
            "https://www.boerse-online.de/index/historisch/s&p_500",
            "https://www.boerse-online.de/index/historisch/tecdax",
        ]
        calculated_index_list = db.create_active_index_url_list(
            cst.URL_INDEX_HISTORY, cst.TEST_DATABASE
        )
        self.assertEqual(asserted_index_list.sort(), calculated_index_list.sort())

    # create stock url list
    def test_create_stock_history_url_list(self):
        asserted_index_list = [
            "https://www.boerse-online.de/kurse/historisch/3i/FSE",
            "https://www.boerse-online.de/kurse/historisch/3m/FSE",
            "https://www.boerse-online.de/kurse/historisch/ab_inbev/FSE",
            "https://www.boerse-online.de/kurse/historisch/adidas/FSE",
            "https://www.boerse-online.de/kurse/historisch/africa-israel_investments/NASO",
            "https://www.boerse-online.de/kurse/historisch/afyon_cimento_sanayii_tas/FSE",
            "https://www.boerse-online.de/kurse/historisch/bechtle/FSE",
            "https://www.boerse-online.de/kurse/historisch/cellcom_israel/FSE",
            "https://www.boerse-online.de/kurse/historisch/coca-cola/FSE",
        ]
        calculated_index_list = db.create_stock_url_list(
            cst.URL_STOCK_HISTORY, cst.TEST_DATABASE
        )
        self.assertEqual(asserted_index_list.sort(), calculated_index_list.sort())

    def test_create_stock_overview_url_list(self):
        asserted_index_list = [
            "https://www.boerse-online.de/aktie/3i-Aktie",
            "https://www.boerse-online.de/aktie/3m-Aktie",
            "https://www.boerse-online.de/aktie/ab_inbev-Aktie",
            "https://www.boerse-online.de/aktie/adidas-Aktie",
            "https://www.boerse-online.de/aktie/africa-israel_investments-Aktie",
            "https://www.boerse-online.de/aktie/afyon_cimento_sanayii_tas-Aktie",
            "https://www.boerse-online.de/aktie/bechtle-Aktie",
            "https://www.boerse-online.de/aktie/cellcom_israel-Aktie",
            "https://www.boerse-online.de/aktie/coca-cola-Aktie",
        ]
        calculated_index_list = db.create_stock_url_list(
            cst.URL_STOCK_OVERVIEW, cst.TEST_DATABASE
        )
        self.assertEqual(asserted_index_list.sort(), calculated_index_list.sort())

    def test_create_stock_info_url_list(self):
        asserted_index_list = [
            "https://www.boerse-online.de/bilanz_guv/3i",
            "https://www.boerse-online.de/bilanz_guv/3m",
            "https://www.boerse-online.de/bilanz_guv/ab_inbev",
            "https://www.boerse-online.de/bilanz_guv/adidas",
            "https://www.boerse-online.de/bilanz_guv/africa-israel_investments",
            "https://www.boerse-online.de/bilanz_guv/afyon_cimento_sanayii_tas",
            "https://www.boerse-online.de/bilanz_guv/bechtle",
            "https://www.boerse-online.de/bilanz_guv/cellcom_israel",
            "https://www.boerse-online.de/bilanz_guv/coca-cola",
        ]
        calculated_index_list = db.create_stock_url_list(
            cst.URL_STOCK_BALANCE, cst.TEST_DATABASE
        )
        self.assertEqual(asserted_index_list.sort(), calculated_index_list.sort())

    # ToDo Clean, refactor, delete from here

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

    # write
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
        self.assertEqual(
            asserted_database_content.sort(), converted_validating_list.sort()
        )

    # Upsert Tests
    def test_upsert_new_single_overview_data_to_db(self):
        current_date = "2019-03-23"
        stock_uri = "coca-cola-Aktie"
        market_cap = "171390.00"
        stock_indices = [
            "Dow Jones",
            "S&P 500",
            "S&P 100",
            "NYSE US 100",
            "IGPA",
            "BX Swiss - USA",
        ]
        stock_sectors = '["Getränke / Tabak"]'

        db.upsert_item(
            table=cst.TABLE_COMPANY_DATA,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            stock_uri=stock_uri,
            market_cap=market_cap,
            current_date=current_date,
            stock_indices=str(stock_indices),
            stock_sectors=str(stock_sectors),
        )

        asserted_company_data_content_after = [
            ["3i-Aktie", '["FTSE 100", "FTSE Allshare"]', '["Finanzdienstleister"]'],
            [
                "ab_inbev-Aktie",
                '["EURO STOXX 50", "STOXX 50", "BEL 20", "EURONEXT 100", "EURO STOXX", "Next CAC 70", "BX Swiss -  EMEA"]',
                '["Getränke / Tabak"]',
            ],
            [
                "ab_inbev-Aktie",
                '["STOXX 50", "EURO STOXX 50", "BEL 20", "EURONEXT 100", "EURO STOXX", "Next CAC 70", "BX Swiss -  EMEA"]',
                '["Getränke / Tabak"]',
            ],
            [
                "bechtle-Aktie",
                '["TecDAX", "MDAX", "Prime All Share", "LMDAX", "Technology All Share", "HDAX", "LTecDAX", "CDAX", "MDAX Kursindex", "TecDAX Kursindex", "BX Swiss - EMEA", "DAXglobal Sarasin Sustainability Germany Index EUR", "QIX Deutschland", "DAXglobal Sarasin Sustainability Germany", "Schatten-Index-SDAX", "Schatten-Index-TecDAX"]',
                '["IT-Dienstleister", "IT-Beratung Hardware", "Dienstleistungen", "Internethandel (B2B, B2C)", "Informationstechnologie"]',
            ],
            [
                "cellcom_israel-Aktie",
                '["TA-100"]',
                '["Telekommunikation", "Mobilkommunikation", "Netzbetreiber (Carrier)", "IT-Dienstleister"]',
            ],
            [
                "coca-cola-Aktie",
                "['Dow Jones', 'S&P 500', 'S&P 100', 'NYSE US 100', 'IGPA', 'BX Swiss - USA']",
                '["Getränke / Tabak"]',
            ],
        ]

        self.assertEqual(
            asserted_company_data_content_after,
            db.get_list(
                table=cst.TABLE_COMPANY_DATA,
                columns=[cst.COLUMN_STOCK_URI, cst.COLUMN_INDICES, cst.COLUMN_SECTORS],
                database=cst.TEST_DATABASE,
            ),
        )

    def test_upsert_existing_single_overview_data_to_db(self):
        stock_uri = "bechtle-Aktie"
        market_cap = "3230.00"
        current_date = "2019-03-16"
        stock_indices = ["TecDAX", "MDAX", "Prime All Share"]

        stock_sectors = [
            "IT-Dienstleister",
            "IT-Beratung Hardware",
            "Dienstleistungen",
            "Internethandel (B2B, B2C)",
            "Informationstechnologie",
        ]

        db.upsert_item(
            table=cst.TABLE_COMPANY_DATA,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            stock_uri=stock_uri,
            market_cap=market_cap,
            current_date=current_date,
            stock_indices=str(stock_indices),
            stock_sectors=str(stock_sectors),
        )

        asserted_data = ["['TecDAX', 'MDAX', 'Prime All Share']"]

        self.assertEqual(
            asserted_data,
            db.get_list(
                table=cst.TABLE_COMPANY_DATA,
                columns=cst.COLUMN_INDICES,
                condition=[cst.COLUMN_STOCK_URI, "bechtle-Aktie"],
                database=cst.TEST_DATABASE,
            ),
        )

    def test_upsert_new_single_balance_data_to_db(self):
        current_date = "2019-03-23"
        stock_uri = "coca-cola-Aktie"
        earnings_at = 6434.00
        operative_result = 9652.00
        sales_revenue = 31697.00
        balance = 83216.00
        equity_capital = 19058.00
        eps_m3 = 1.51
        eps_m2 = 0.29
        eps_m1 = 1.51

        db.upsert_item(
            table=cst.TABLE_COMPANY_DATA,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            earnings_after_tax=earnings_at,
            operative_result=operative_result,
            sales_revenue=sales_revenue,
            balance=balance,
            equity_capital=equity_capital,
            eps_m3=eps_m3,
            eps_m2=eps_m2,
            eps_m1=eps_m1,
        )

        self.assertEqual(
            "1.51",
            str(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_EPS_M3,
                    condition=[cst.COLUMN_STOCK_URI, "coca-cola-Aktie"],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_existing_single_balance_data_to_db(self):
        current_date = "2019-03-09"
        stock_uri = "ab_inbev-Aktie"
        equity_capital = 121541.00
        earnings_at = 3702.48
        operative_result = 14520.88

        db.upsert_item(
            table=cst.TABLE_COMPANY_DATA,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            equity_capital=equity_capital,
            earnings_after_tax=earnings_at,
            operative_result=operative_result,
        )

        self.assertEqual(
            "3702.48",
            str(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_EARNINGS_AT,
                    condition=[cst.COLUMN_EQUITY_CAPITAL, 121541.00],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_new_roe(self):
        current_date = "2019-03-30"
        stock_uri = "ab_inbev-Aktie"
        return_on_equity = "0.06"
        lev_01_score = "-1"

        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            lev_01_val=return_on_equity,
            lev_01_sco=lev_01_score,
        )

        self.assertEqual(
            return_on_equity,
            str(
                db.get_item(
                    table=cst.TABLE_LEVERMANN,
                    column=cst.COLUMN_LEV01_VALUE,
                    condition=[cst.COLUMN_DATE, "2019-03-30"],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_existing_roe(self):
        current_date = "2019-03-23"
        stock_uri = "ab_inbev-Aktie"
        return_on_equity = "0.08"
        lev_01_score = "-1"

        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            lev_01_val=return_on_equity,
            lev_01_sco=lev_01_score,
        )

        self.assertEqual(
            return_on_equity,
            str(
                db.get_item(
                    table=cst.TABLE_LEVERMANN,
                    column=cst.COLUMN_LEV01_VALUE,
                    condition=[cst.COLUMN_DATE, "2019-03-23"],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_new_ebit(self):
        current_date = "2019-03-30"
        stock_uri = "ab_inbev-Aktie"
        ebit = "0.32"
        lev_02_score = "1"

        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            lev_02_val=ebit,
            lev_02_sco=lev_02_score,
        )

        self.assertEqual(
            ebit,
            str(
                db.get_item(
                    table=cst.TABLE_LEVERMANN,
                    column=cst.COLUMN_LEV02_VALUE,
                    condition=[cst.COLUMN_DATE, "2019-03-30"],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_new_kgv5(self):
        current_date = "2019-03-30"
        stock_uri = "ab_inbev-Aktie"
        kgv5 = "24.91"
        lev_04_score = "-1"

        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            database=cst.TEST_DATABASE,
            current_date=current_date,
            stock_uri=stock_uri,
            lev_04_val=kgv5,
            lev_04_sco=lev_04_score,
        )

        self.assertEqual(
            kgv5,
            str(
                db.get_item(
                    table=cst.TABLE_LEVERMANN,
                    column=cst.COLUMN_LEV04_VALUE,
                    condition=[cst.COLUMN_DATE, "2019-03-30"],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_upsert_new_targets(self):
        current_date = "2019-03-09"
        stock_uri = "ab_inbev-Aktie"
        buy, hold, sell = 7, 1, 0

        db.upsert_item(
            table=cst.TABLE_COMPANY_DATA,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            stock_uri=stock_uri,
            current_date=current_date,
            analyst_buy=buy,
            analyst_hold=hold,
            analyst_sell=sell,
            database=cst.TEST_DATABASE,
        )

        self.assertEqual(
            buy,
            db.get_item(
                table=cst.TABLE_COMPANY_DATA,
                column=cst.COLUMN_ANALYST_BUY,
                condition=[cst.COLUMN_DATE, "2019-03-09"],
                database=cst.TEST_DATABASE,
            ),
        )

        self.assertEqual(
            hold,
            db.get_item(
                table=cst.TABLE_COMPANY_DATA,
                column=cst.COLUMN_ANALYST_HOLD,
                condition=[cst.COLUMN_DATE, "2019-03-09"],
                database=cst.TEST_DATABASE,
            ),
        )

        self.assertEqual(
            sell,
            db.get_item(
                table=cst.TABLE_COMPANY_DATA,
                column=cst.COLUMN_ANALYST_SELL,
                condition=[cst.COLUMN_DATE, "2019-03-09"],
                database=cst.TEST_DATABASE,
            ),
        )

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # Space for upsert_item Tests
    #
    #
    #
    #
    #

    def test_quarterly_date_upsert(self):
        # ToDo
        pass

    # Update Tests
    def test_update_existing_stocks_market_place(self):
        stock_uri = "coca-cola-Aktie"
        market_place = "XETRA"

        db.update_item(
            table=cst.TABLE_STOCKS,
            primary_keys=cst.COLUMN_URI,
            database=cst.TEST_DATABASE,
            uri=stock_uri,
            market_place=market_place,
        )

        asserted_data = ["XETRA"]

        self.assertEqual(
            asserted_data,
            db.get_list(
                table=cst.TABLE_STOCKS,
                columns=cst.COLUMN_MARKET_PLACE,
                condition=[cst.COLUMN_URI, "coca-cola-Aktie"],
                database=cst.TEST_DATABASE,
            ),
        )

    def test_update_not_existing_stocks_market_place(self):
        stock_uri = "new-Aktie"
        market_place = "XETRA"

        result = db.update_item(
            table=cst.TABLE_STOCKS,
            primary_keys=cst.COLUMN_URI,
            database=cst.TEST_DATABASE,
            uri=stock_uri,
            market_place=market_place,
        )

        self.assertFalse(result)

    # insert ignore/many
    def test_write_index_content_to_stock_table(self):
        stock_list = [
            ["3i", "3i-Aktie"],
            ["Admiral Group", "admiral_group-Aktie"],
            ["Anglo American", "anglo_american-Aktie"],
        ]
        index_uri = "FTSE_100"
        asserted_stock_list_before = [
            "3i-Aktie",
            "3m-Aktie",
            "ab_inbev-Aktie",
            "adidas-Aktie",
            "africa-israel_investments-Aktie",
            "afyon_cimento_sanayii_tas-Aktie",
            "bechtle-Aktie",
            "cellcom_israel-Aktie",
            "coca-cola-Aktie",
        ]
        self.assertEqual(
            asserted_stock_list_before,
            db.get_list(
                table=cst.TABLE_STOCKS,
                columns=cst.COLUMN_URI,
                database=cst.TEST_DATABASE,
            ),
        )

        db.write_index_content_list_to_db(stock_list, index_uri, cst.TEST_DATABASE)

        asserted_stock_list_after = [
            "3i-Aktie",
            "3i-Aktie",
            "admiral_group-Aktie",
            "anglo_american-Aktie",
        ]

        self.assertEqual(
            asserted_stock_list_after,
            db.get_list(
                table=cst.TABLE_INDEX_CONTENTS,
                columns=cst.COLUMN_STOCK_URI,
                condition=[cst.COLUMN_INDEX_URI, "FTSE_100"],
                database=cst.TEST_DATABASE,
            ),
        )

    # uncategorized tests
    def test_convert_list_to_db_value_string(self):
        input_data_list = [
            ["adidas-Aktie", "07.11.18", "Quartalszahlen", "Future"],
            ["adidas-Aktie", "07.03.19", "Quartalszahlen", "Future"],
            ["adidas-Aktie", "02.05.19", "Quartalszahlen", "Future"],
        ]
        asserted_list_string = (
            "('adidas-Aktie', '07.11.18', 'Quartalszahlen', 'Future'), "
            "('adidas-Aktie', '07.03.19', 'Quartalszahlen', 'Future'), "
            "('adidas-Aktie', '02.05.19', 'Quartalszahlen', 'Future')"
        )
        self.assertEqual(
            asserted_list_string, db.convert_list_to_db_value_string(input_data_list)
        )

        input_data_list_2 = [["adidas-Aktie", "07.11.18", "Quartalszahlen", "Future"]]
        asserted_list_string_2 = (
            "('adidas-Aktie', '07.11.18', 'Quartalszahlen', 'Future')"
        )
        self.assertEqual(
            asserted_list_string_2,
            db.convert_list_to_db_value_string(input_data_list_2),
        )

    def test_insert_future_dates_table(self):
        rv = db.insert_list(
            table="Aktientermine",
            data=[
                ["adidas-Aktie", "2018-11-07", "Quartalszahlen", "Future"],
                ["adidas-Aktie", "2018-03-07", "Quartalszahlen", "Future"],
                ["adidas-Aktie", "2019-05-02", "Quartalszahlen", "Future"],
            ],
            database=cst.TEST_DATABASE,
        )
        self.assertTrue(rv)

    def test_insert_past_dates_table(self):
        rv = db.insert_list(
            table="Aktientermine",
            data=[
                ["adidas-Aktie", "2018-08-09", "Q2 2018 Earnings Release", "Past"],
                ["adidas-Aktie", "2018-05-09", "Hauptversammlung", "Past"],
                ["adidas-Aktie", "2017-11-09", "Q3 2017", "Past"],
            ],
            database=cst.TEST_DATABASE,
        )
        self.assertTrue(rv)

    # Get_Item Tests

    # def test_get_earnings_after_tax(self):
    #     result = db.get_earnings_after_tax("ab_inbev-Aktie", database=cst.TEST_DATABASE)
    #     self.assertEqual(3702.48, result)

    def test_get_earnings_after_tax(self):
        self.assertEqual(
            3702.48,
            float(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_EARNINGS_AT,
                    condition=[cst.COLUMN_STOCK_URI, "ab_inbev-Aktie"],
                    order=[cst.COLUMN_DATE, cst.DESC],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    # def test_get_equity_capital(self):
    #     result = db.get_equity_capital("ab_inbev-Aktie", database=cst.TEST_DATABASE)
    #     self.assertEqual(62899.88, result)

    def test_get_equity_capital(self):
        self.assertEqual(
            62899.88,
            float(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_EQUITY_CAPITAL,
                    condition=[cst.COLUMN_STOCK_URI, "ab_inbev-Aktie"],
                    order=[cst.COLUMN_DATE, cst.DESC],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_get_operative_result(self):
        self.assertEqual(
            14520.88,
            float(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_OPERATIVE_RESULT,
                    condition=[cst.COLUMN_STOCK_URI, "ab_inbev-Aktie"],
                    order=[cst.COLUMN_DATE, cst.DESC],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_get_sales_revenue(self):
        self.assertEqual(
            46297.11,
            float(
                db.get_item(
                    table=cst.TABLE_COMPANY_DATA,
                    column=cst.COLUMN_SALES_REVENUE,
                    condition=[cst.COLUMN_STOCK_URI, "ab_inbev-Aktie"],
                    order=[cst.COLUMN_DATE, cst.DESC],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_get_latest_stock_price(self):
        self.assertEqual(
            199.40,
            float(
                db.get_item(
                    table=cst.TABLE_STOCKS_HISTORIES,
                    column=cst.COLUMN_CLOSING_VALUE,
                    condition=[cst.COLUMN_STOCK_URI, "adidas-Aktie"],
                    order=[cst.COLUMN_DATE, cst.DESC],
                    database=cst.TEST_DATABASE,
                )
            ),
        )

    def test_get_quarterly_date(self):
        asserted_date = date.string_to_date("21.03.2019")
        self.assertEqual(
            asserted_date,
            db.get_item(
                table=cst.TABLE_STOCK_DATES,
                column=cst.COLUMN_DATE,
                condition=[cst.COLUMN_STOCK_URI, "ab_inbev-Aktie"],
                order=[cst.COLUMN_DATE, cst.DESC],
                database=cst.TEST_DATABASE,
            ),
        )

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # Space for get_item Tests
    #
    #
    #
    #
    #

    # Get_list Tests

    def test_get_current_eps_s(self):
        eps_s = db.get_latest_eps("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual([0.65, 3.60, 1.87, 4.13, 4.48], eps_s)

    def test_get_current_eps_s_if_is_none(self):
        eps_s = db.get_latest_eps("empty-Aktie", database=cst.TEST_DATABASE)
        self.assertIsNone(eps_s)

    def test_get_last_eps_s(self):
        eps_s = db.get_second_latest_eps("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual([0.65, 3.60, 1.87, 4.11, 4.49], eps_s)

    def test_ratings(self):
        ratings = db.get_analyst_ratings("ab_inbev-Aktie", database=cst.TEST_DATABASE)
        self.assertEqual([6, 2, 0], ratings)

    def test_caps_large(self):
        is_small_cap = db.is_small_cap(
            stock_uri="ab_inbev-Aktie", database=cst.TEST_DATABASE
        )
        self.assertFalse(is_small_cap)

    def test_caps_small(self):
        is_small_cap = db.is_small_cap(
            stock_uri="bechtle-Aktie", database=cst.TEST_DATABASE
        )
        self.assertTrue(is_small_cap)

    def test_get_closing_stock_price_with_date_available(self):
        stock_uri = "adidas-Aktie"
        quarterly = date.string_to_date("29.01.2019")
        closing_price, actual_date = db.get_closing_stock_price(
            quarterly, stock_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(204.90, float(closing_price))

    def test_get_closing_stock_price_with_date_not_available(self):
        stock_uri = "adidas-Aktie"
        quarterly_we = "2019-02-03"
        closing_price, actual_date = db.get_closing_stock_price(
            quarterly_we, stock_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(199.40, float(closing_price))
        self.assertEqual("01.02.2019", date.date_to_string(actual_date))

    def test_get_closing_index_price_with_date_available(self):
        index_uri = "dax"
        quarterly = "2019-03-07"
        closing_price, actual_date = db.get_closing_index_price(
            quarterly, index_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(11546.42, float(closing_price))

    def test_get_closing_index_price_with_date_not_available(self):
        index_uri = "dax"
        quarterly_we = "2019-03-10"
        closing_price, actual_date = db.get_closing_index_price(
            quarterly_we, index_uri, database=cst.TEST_DATABASE
        )
        self.assertEqual(11429.77, float(closing_price))
        self.assertEqual("08.03.2019", date.date_to_string(actual_date))

    def test_get_main_index_of_stock(self):
        stock_uri = "3i-Aktie"
        index_uri = db.get_main_index_of_stock(stock_uri, database=cst.TEST_DATABASE)
        self.assertEqual("FTSE_100", index_uri)

    def test_get_main_index_of_stock_when_stock_not_exists(self):
        stock_uri = "3m-Aktie"
        index_uri = db.get_main_index_of_stock(stock_uri, database=cst.TEST_DATABASE)
        self.assertIsNone(index_uri)

    def test_get_main_index_of_stock_when_index_is_not_existent(self):
        stock_uri = "cellcom_israel-Aktie"
        index_uri = db.get_main_index_of_stock(stock_uri, database=cst.TEST_DATABASE)
        self.assertIsNone(index_uri)

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
        # db_test.delete_test_data()
        # db_test.drop_test_tables()
        pass


if __name__ == "__main__":
    unittest.main()
